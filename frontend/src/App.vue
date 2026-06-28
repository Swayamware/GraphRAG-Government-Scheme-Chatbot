<template>
  <div class="h-screen w-screen overflow-hidden bg-slate-950 text-slate-100 flex">
    <Chat class="w-full h-full" />
  </div>
</template>

<script setup>
import Chat from './components/Chat.vue'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

body {
  margin: 0;
  padding: 0;
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: #020617; /* slate-950 */
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Outfit', sans-serif;
}
</style>
