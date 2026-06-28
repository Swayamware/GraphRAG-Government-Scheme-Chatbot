from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

try:
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        record = result.single()
        print("NODE_COUNT:", record["count"])
except Exception as e:
    print("ERROR:", e)
finally:
    driver.close()
