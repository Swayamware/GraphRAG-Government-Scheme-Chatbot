<template>
  <div class="flex h-screen w-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
    
    <!-- Sidebar -->
    <div class="w-80 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0">
      
      <!-- Sidebar Header -->
      <div class="p-6 border-b border-slate-800">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
            <!-- Bot Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
          </div>
          <div>
            <h1 class="font-bold text-lg tracking-tight text-white">GovSchemes</h1>
            <p class="text-xs text-slate-400">Graph-based RAG Portal</p>
          </div>
        </div>
      </div>

      <!-- Chat History list -->
      <div class="flex-1 overflow-y-auto px-4 py-4 space-y-2 custom-scroll">
        <h3 class="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Saved Sessions</h3>
        
        <div
          v-for="(chat, index) in chats"
          :key="chat.id"
          @click="switchChat(index)"
          class="group flex items-center justify-between px-3 py-3 cursor-pointer rounded-xl transition-all duration-200 border"
          :class="activeChatIndex === index 
            ? 'bg-indigo-600/10 border-indigo-500/50 text-white shadow-md shadow-indigo-950/20' 
            : 'border-transparent hover:bg-slate-800/60 text-slate-400 hover:text-slate-200'"
        >
          <div class="flex items-center gap-3 truncate">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0" :class="activeChatIndex === index ? 'text-indigo-400' : 'text-slate-500'"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <span class="text-sm font-medium truncate">Session {{ index + 1 }}</span>
          </div>
          
          <button
            @click.stop="deleteChat(index)"
            class="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-500 hover:text-red-400 hover:bg-slate-800/80 transition-all duration-150"
            title="Delete session"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
          </button>
        </div>
      </div>

      <!-- Sidebar Footer / New Session Button -->
      <div class="p-6 border-t border-slate-800">
        <button
          @click="newChat"
          class="w-full py-3 rounded-xl font-semibold transition-all duration-200 bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white shadow-lg shadow-indigo-950/50 flex items-center justify-center gap-2 text-sm border border-indigo-400/20"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
          New Session
        </button>
      </div>
    </div>

    <!-- Main Chat Window -->
    <div class="flex-1 flex flex-col bg-slate-950 relative overflow-hidden">
      <!-- Glow background decoration -->
      <div class="absolute w-[500px] h-[500px] rounded-full bg-indigo-500/5 blur-[120px] top-[-250px] right-[-100px] pointer-events-none"></div>
      <div class="absolute w-[500px] h-[500px] rounded-full bg-emerald-500/5 blur-[120px] bottom-[-200px] left-[-200px] pointer-events-none"></div>

      <!-- Header -->
      <div class="px-8 py-5 border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md flex justify-between items-center z-10">
        <div class="flex items-center gap-3">
          <div>
            <h2 class="font-bold text-base text-white">Active Session</h2>
            <p class="text-xs text-slate-400 flex items-center gap-1.5">
              <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              LLM & Neo4j Systems Ready
            </p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <!-- Language Selector -->
          <div class="flex items-center bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5">
            <span class="text-xs text-slate-400 mr-2 font-medium">Input Lang:</span>
            <select 
              v-model="speechLang" 
              class="bg-transparent text-sm text-white font-medium focus:outline-none cursor-pointer"
            >
              <option value="en-IN" class="bg-slate-950">English</option>
              <option value="mr-IN" class="bg-slate-950">मराठी (Marathi)</option>
            </select>
          </div>

          <!-- End Chat Button -->
          <button
            @click="endChat"
            class="px-4 py-2 rounded-xl text-sm font-semibold border border-red-500/30 bg-red-500/10 hover:bg-red-500/20 text-red-400 transition-all duration-200"
          >
            End Session
          </button>
        </div>
      </div>

      <!-- Message Area -->
      <div ref="chatWindow" class="flex-1 overflow-y-auto p-8 space-y-6 custom-scroll z-10">
        
        <!-- Welcome prompt when chat is empty -->
        <div 
          v-if="!chats[activeChatIndex]?.messages || chats[activeChatIndex].messages.length === 0" 
          class="h-full flex flex-col items-center justify-center max-w-lg mx-auto text-center space-y-6 pt-12"
        >
          <div class="p-4 rounded-3xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 w-16 h-16 flex items-center justify-center shadow-inner">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-bounce"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-white tracking-tight mb-2">Welcome to Government Schemes RAG Portal</h3>
            <p class="text-slate-400 text-sm leading-relaxed">
              Ask about national or state-level schemes, including welfare, health, scholarships, and employment. Queries will search a live Neo4j knowledge graph using Mistral LLM translation.
            </p>
          </div>
          
          <div class="grid grid-cols-2 gap-3 w-full text-left">
            <div 
              v-for="prompt in suggestedPrompts" 
              :key="prompt"
              @click="useSuggestedPrompt(prompt)"
              class="p-3 bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-slate-700 rounded-xl cursor-pointer transition text-xs text-slate-300 font-medium"
            >
              {{ prompt }}
            </div>
          </div>
        </div>

        <!-- Render active chat messages -->
        <div
          v-for="(msg, idx) in chats[activeChatIndex]?.messages || []"
          :key="idx"
          :class="msg.sender === 'user' ? 'flex justify-end' : 'flex justify-start'"
          class="transition-all duration-300"
        >
          <div class="max-w-2xl flex flex-col gap-1.5">
            <!-- Sender tag -->
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider px-1">
              {{ msg.sender === 'user' ? 'You' : 'System Bot' }}
            </span>

            <div
              :class="[
                'px-5 py-3.5 rounded-2xl shadow-lg border text-sm md:text-base leading-relaxed',
                msg.sender === 'user'
                  ? 'bg-indigo-600/10 border-indigo-500/30 text-indigo-100 rounded-tr-none'
                  : 'bg-slate-900 border-slate-800 text-slate-200 rounded-tl-none'
              ]"
            >
              <!-- List of schemes parsed as cards -->
              <template v-if="msg.type === 'list'">
                <div class="space-y-4">
                  <div class="text-xs text-indigo-400 font-semibold flex items-center gap-1.5 border-b border-slate-800 pb-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg>
                    Matching graph database results:
                  </div>
                  
                  <div class="grid gap-3">
                    <div 
                      v-for="(item, i) in parsedList(msg.text)" 
                      :key="i"
                      class="p-4 bg-slate-950/60 rounded-xl border border-slate-800 hover:border-indigo-500/20 transition-all hover:bg-slate-950"
                    >
                      <div class="font-bold text-white text-base mb-1.5 flex items-start justify-between gap-4">
                        <span>{{ item.title }}</span>
                        <div class="flex items-center gap-1.5 shrink-0 flex-wrap">
                          <span 
                            v-if="item.schemeBy" 
                            class="px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
                          >
                            {{ item.schemeBy }}
                          </span>
                          <span 
                            v-if="item.location" 
                            class="px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                          >
                            {{ item.location }}
                          </span>
                          <span 
                            v-if="!item.schemeBy && !item.location" 
                            class="px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider bg-slate-500/10 text-slate-400 border border-slate-500/20"
                          >
                            Active
                          </span>
                        </div>
                      </div>
                      <p v-if="item.body" class="text-sm text-slate-450 leading-relaxed font-normal">
                        {{ item.body }}
                      </p>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Text block -->
              <template v-else>
                <p class="whitespace-pre-line">{{ msg.text }}</p>
              </template>
            </div>
            
            <span 
              class="text-[10px] text-slate-500 mt-0.5 px-1"
              :class="msg.sender === 'user' ? 'text-right' : 'text-left'"
            >
              {{ msg.time }}
            </span>
          </div>
        </div>

        <!-- Typing loader -->
        <div v-if="isTyping" class="flex justify-start">
          <div class="flex flex-col gap-1.5 max-w-xs">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider">System Bot</span>
            <div class="px-5 py-4 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 rounded-tl-none flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-2.5 h-2.5 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-2.5 h-2.5 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>

      </div>

      <!-- Input Section -->
      <div class="p-6 border-t border-slate-800/80 bg-slate-900/20 backdrop-blur-md z-10">
        <form @submit.prevent="sendQuestion" class="max-w-4xl mx-auto flex items-center gap-3">
          
          <div class="flex-1 relative flex items-center bg-slate-900 border border-slate-800 hover:border-slate-700 focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500 rounded-2xl px-4 py-2 transition-all">
            <input
              v-model="question"
              type="text"
              placeholder="Type your question or use Marathi speech..."
              class="flex-1 bg-transparent border-none text-white text-sm md:text-base focus:outline-none py-1.5 placeholder-slate-500"
            />

            <!-- Mic status glowing pulse -->
            <div v-if="listening" class="absolute right-4 w-3.5 h-3.5 rounded-full bg-red-500 animate-ping"></div>
          </div>

          <!-- Mic Button -->
          <button
            type="button"
            @click="toggleListening"
            class="p-3.5 rounded-xl border transition-all duration-200 shrink-0"
            :class="listening 
              ? 'bg-red-500/10 border-red-500/40 text-red-400 hover:bg-red-500/20' 
              : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-850'"
            :title="listening ? 'Stop Microphone' : 'Use Speech Recognition'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="{ 'animate-pulse text-red-500': listening }"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
          </button>

          <!-- Submit Button -->
          <button
            type="submit"
            class="px-6 py-3.5 rounded-xl font-bold bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-lg shadow-indigo-950/40 flex items-center justify-center gap-2 text-sm shrink-0 border border-indigo-400/20"
          >
            <span>Ask Graph</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" x2="11" y1="2" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import axios from 'axios'

const question = ref('')
const speechLang = ref('en-IN')
const listening = ref(false)
const isSpeechInput = ref(false)
const isTyping = ref(false)

const chats = ref([{ id: Date.now(), messages: [] }])
const activeChatIndex = ref(0)

const suggestedPrompts = [
  'health schemes for women in bihar',
  'scholarship schemes for students in maharashtra',
  'employment schemes for youth in delhi',
  'number of central schemes'
]

let recognition = null
const chatWindow = ref(null)

watch(
  () => chats.value[activeChatIndex.value]?.messages,
  async () => {
    await nextTick()
    scrollToBottom()
  },
  { deep: true }
)

function scrollToBottom() {
  if (chatWindow.value) {
    chatWindow.value.scrollTo({
      top: chatWindow.value.scrollHeight,
      behavior: 'smooth'
    })
  }
}

function useSuggestedPrompt(prompt) {
  question.value = prompt
}

function parsedList(text) {
  try {
    const rawList = Array.isArray(text) ? text : JSON.parse(text)
    return rawList.map(item => {
      if (typeof item === 'object' && item !== null) {
        return {
          title: item.name || 'Scheme Name Not Specified',
          body: item.objective || item.description || '',
          location: item.location || '',
          schemeBy: item.scheme_by || ''
        }
      }
      
      if (typeof item === 'string') {
        const idx = item.indexOf(': ')
        if (idx !== -1) {
          return {
            title: item.substring(0, idx),
            body: item.substring(idx + 2),
            location: '',
            schemeBy: ''
          }
        }
        return { title: item, body: '', location: '', schemeBy: '' }
      }
      return { title: String(item), body: '', location: '', schemeBy: '' }
    })
  } catch {
    return [{ title: text, body: '', location: '', schemeBy: '' }]
  }
}

// Speech recognition setup
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  recognition = new SpeechRecognition()
  recognition.interimResults = false
  recognition.maxAlternatives = 1

  recognition.onresult = (event) => {
    question.value = event.results[0][0].transcript
    listening.value = false
    isSpeechInput.value = true
    sendQuestion()
  }
  recognition.onerror = () => (listening.value = false)
  recognition.onend = () => (listening.value = false)
}

function toggleListening() {
  if (!recognition) return alert('Speech recognition is not supported in this browser.')
  
  if (listening.value) {
    recognition.stop()
  } else {
    recognition.lang = speechLang.value 
    recognition.start()
  }
  
  listening.value = !listening.value
}

async function sendQuestion() {
  if (!question.value.trim()) return
  
  const userMessage = question.value
  chats.value[activeChatIndex.value].messages.push({
    sender: 'user',
    text: userMessage,
    type: 'text',
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  })
  
  question.value = ''
  isTyping.value = true
  scrollToBottom()

  try {
    const res = await axios.post('http://127.0.0.1:5000/ask', {
      question: userMessage,
      speech_mode: isSpeechInput.value,
      speech_lang: speechLang.value
    })
    
    chats.value[activeChatIndex.value].messages.push({
      sender: 'bot',
      text: res.data.answer,
      type: res.data.type || 'text',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })
    saveChats()
  } catch (err) {
    chats.value[activeChatIndex.value].messages.push({
      sender: 'bot',
      text: err.response?.data?.error || 'Failed to connect to the backend server. Please verify app.py is running.',
      type: 'text',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })
  } finally {
    isTyping.value = false
    isSpeechInput.value = false
    scrollToBottom()
  }
}

function newChat() {
  chats.value.push({ id: Date.now(), messages: [] })
  activeChatIndex.value = chats.value.length - 1
  saveChats()
}

function switchChat(index) {
  activeChatIndex.value = index
}

function endChat() {
  chats.value[activeChatIndex.value].messages.push({
    sender: 'bot',
    text: '🔒 Session has been finalized.',
    type: 'text',
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  })
  saveChats()
}

function deleteChat(index) {
  chats.value.splice(index, 1)
  if (activeChatIndex.value >= chats.value.length) activeChatIndex.value = chats.value.length - 1
  if (chats.value.length === 0) newChat()
  saveChats()
}

// LocalStorage persistence
function saveChats() {
  localStorage.setItem('mkcl_chats', JSON.stringify(chats.value))
}

function loadChats() {
  const saved = localStorage.getItem('mkcl_chats')
  if (saved) chats.value = JSON.parse(saved)
}

loadChats()
</script>

<style>
/* Custom scrollbar matching slate colors */
.custom-scroll::-webkit-scrollbar {
  width: 6px;
}
.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background: #334155; /* slate-700 */
  border-radius: 9999px;
}
.custom-scroll::-webkit-scrollbar-thumb:hover {
  background: #475569; /* slate-600 */
}
</style>
