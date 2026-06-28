import sys
import subprocess
from backend.cypher_generator import generate_cypher_query

try:
    print("Testing generate_cypher_query:")
    q = generate_cypher_query("what schemes are there for farmers?")
    print(f"Result: {q}")
except Exception as e:
    print(f"Error: {e}")
