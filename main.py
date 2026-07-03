import os
import json
import google.generativeai as genai

# 1. Read the key from the environment — NEVER hardcode it.
#    Set it first in your shell:  export GEMINI_API_KEY="your-new-key"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- Input: just a hardcoded list for v1. Fancy input is v2. ---
tasks = [
    "Pour the foundation",
    "Frame the walls",
    "Install the roof",
    "Run electrical wiring",
    "Paint the interior",
]

# 2. ONE structured call: give it all tasks, ask for edges as JSON.
# model = genai.GenerativeModel("gemini-flash-latest")
model = genai.GenerativeModel("gemini-2.5-flash")

prompt = f"""You are given a list of tasks. Determine the dependency relationships between them.
A dependency "A -> B" means task A must be completed before task B can begin.

Return ONLY a JSON array of edges, where each edge is an object with "from" and "to" keys
using the exact task text. Include an edge only when there is a real dependency.
Do not include any explanation, only the JSON.

Tasks:
{json.dumps(tasks, indent=2)}
"""

response = model.generate_content(
    prompt,
    generation_config={"response_mime_type": "application/json"},  # <-- structured JSON mode
)

# 3. Parse the JSON edges.
edges = json.loads(response.text)
print("Dependencies found:")
for edge in edges:
    print(f"  {edge['from']} -> {edge['to']}")

# 4. Render the graph with graphviz.
from graphviz import Digraph

dot = Digraph(comment="Task Dependencies")
for task in tasks:
    dot.node(task, task)
for edge in edges:
    dot.edge(edge["from"], edge["to"])

dot.render("dependency_graph", format="png", cleanup=True)
print("\nGraph saved to dependency_graph.png")
