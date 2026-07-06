# the next thing i code will be going back to handing the program a list of tasks rather than a singular project goal. submodule out what we have and bring back the old functionality.
# also wanna remove redundant dependencies via transitive: A->B and B->C implies A->C, so we don't explicitly need A->C.
# also wanna recursively decompose compound problems like "return home and reflect on your trip".
# a summary would be nice
# prune orphans
# if we go item-by-item, we have to eventually note or potentially resolve circular dependencies.
# also make sure to update to google.genai

import os # pull keys from the env
import json # parse JSON output
import google.generativeai as genai # the model
from graphviz import Digraph # visualization tool


# never hard-code your keys!
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


model = genai.GenerativeModel("gemini-2.5-flash")

# structured=True forces JSON output. used in the formatter stages.
# structured=False lets the model reason freely with arbitrary text output. used in the thinking stages.
def call_model(
    prompt: str,
    structured: bool = False
) -> str:
    return model.generate_content(
        prompt, # string input
        generation_config = {"response_mime_type": "application/json"} if structured else {} # determines if the output should be formatted in JSON
    ).text # just the text of the output as a string



### === INPUT === ###

# ex: "Take a trip to Japan."
# this should eventually be os· input instead of hard-coded

problem = "Build a small house from an empty plot of land."



### === MODEL PIPELINE === ###

# === STAGE 1: Decomposition === #
decomposition = call_model(
    f"""
        Please break the following goal down into its component steps -- that is, the concrete tasks needed to accomplish it.
        Think it through, take your time, and list the steps clearly once you're done.
        Thank you in advance `:)`

        The goal:
        {problem}
    """,
    structured=False)
print("=== STAGE 1: Decomposition ===")
print(decomposition)


# === STAGE 2: Formatting === #
steps = json.loads(call_model(
    f"""
        The following text describes steps for accomplishing a goal.
        Please extract them into a clean list, returning only a JSON array of strings, with each string being one concise step.
        Thank you in advance `:)`
        
        Steps as text:
        {decomposition}
    """,
    structured=True))
print("\n=== STAGE 2: Formatting ===")
for s in steps:
    print(f"- {s}")


# === STAGE 3: Dependency Analysis === #
analysis = call_model(
    f"""
        What follows is a list of steps for accomplishing a goal.
        Please determine the dependency relationships -- that is, for each step, determine which other steps must come before it.
        Take your time, iterate through the list, and reason about the dependencies before finally stating your conclusions.
        Thank you in advance `:)`

        List of steps:
        {json.dumps(steps, indent=2)}
    """,
    structured=False)
print("\n=== STAGE 3: Dependency Analysis ===")
print(analysis)


# === STAGE 4: Extraction === #
edges = json.loads(call_model(
    f"""
        The following text reasons about dependencies between steps.
        Please extract the relationships from the concluded reasoning, returning a JSON array of edges, each an object with "from" and "to" keys.
        Thank you in advance `:)`

        Here are the steps:
        {json.dumps(steps, indent=2)}

        ...and here is the reasoning:
        {analysis}
    """,
    structured=True))
print("\n=== STAGE 4: Extraction ===")
for edge in edges:
    print(f"{edge['from']} -> {edge['to']}")


### === END MODEL PIPELINE === ###


# === RENDERING === #
dot = Digraph(comment="Task Dependencies")

# v3 should combine these steps.
for step in steps:
    dot.node(step, step)
for edge in edges:
    dot.edge(edge["from"], edge["to"])

# eventually, i should make this not hard-coded
dot.render("dependency_graph", format="png", cleanup=True)
print("\nGraph saved to dependency_graph.png")
