# AI Weather Assistant using LangChain
# Introduction to LangChain

> **LangChain is a framework**
> 
> 
> ❗ But it’s **not opinionated like CrewAI**, so it gives *building blocks*, not full boilerplate projects
> 

---

## Difference Between CrewAI and LangChain Framework

## CrewAI style

CrewAI gives you:

- Predefined structure:
    - Agents
    - Tasks
    - Crew
- Almost like a **template/project generator**

👉 You just “fill in blanks”

---

## LangChain style

LangChain gives:

- Low-level primitives:
    - Models
    - Tools
    - Agents
    - Memory

👉 You **assemble things yourself**

---

## Analogy

| Tool | Like |
| --- | --- |
| CrewAI | 🏗️ Ready-made building template |
| LangChain | 🧱 Bricks + cement |

---

## Does LangChain provide boilerplate at all?

👉 Kind of… but not like CrewAI.

It provides:

### 1. Helper functions

```
agent=create_agent(...)
```

👉 This is already **boilerplate abstraction**

---

### 2. Prebuilt agents

- ReAct agents
- Tool-calling agents
- Chat agents

---

### 3. Templates (but scattered)

In:

- GitHub examples
- Docs
- LangGraph projects

---

## Where LangChain becomes “structured”

👉 When you use **LangGraph**

That gives you:

- Node-based workflows
- State management
- Production-ready patterns

👉 That’s closer to **real architecture**

---

## Why LangChain is designed this way

Because it’s meant for:

- Flexibility
- Custom pipelines
- Complex systems

👉 Not just simple agents

---

## Tradeoff

| Framework | Pros | Cons |
| --- | --- | --- |
| CrewAI | Easy, fast | Limited flexibility |
| LangChain | Powerful, flexible | More manual setup |

---

## What we’re currently doing

our project:

```
LLM + Tool + Agent
```

👉 This is **basic LangChain layer**

---

## If you want “boilerplate feel” in LangChain

You can structure like this:

```
project/
│
├── main.py
├── tools/
│   └── weather.py
├── agents/
│   └── weather_agent.py
├── config/
│   └── settings.py
```

👉 Now it starts feeling like a proper framework

---

<aside>
💡

Note:

> 👉 LangChain doesn’t *force* structure
> 
> 
> 👉 CrewAI *imposes* structure
> 
</aside>

# Implementation

For this demo i am using and separte ubuntu VM in Azure.

You can implement the same in the local machine as well.

Install LangChain packages.

```python
pip install -U langchain
```

LangChain provides integrations to hundreds of LLMs and thousands of other integrations. These live in independent provider packages.

```python
# Installing the OpenAI integration
pip install -U langchain-openai

# Installing the Anthropic integration
pip install -U langchain-anthropic
```

I am using Gemini here so i am gonna run the below command.

```python
pip install langchain-google-genai
```

Set `env vars`:

You can get the gemini api keys from [`https://aistudio.google.com/api-keys`](https://aistudio.google.com/api-keys) for free. 

(Use the API carefully it gives very less number of call in the free tier)

```python
export GEMINI_API_KEY=AIz**********************************9Q
export GOOGLE_API_KEY=AIz****************************GzqVNK9Q
```

## **Build a basic agent**

Start by creating a simple agent that can answer questions and call tools. The agent will use Gemini 2.5 Flash as its language model, a basic weather function as a tool, and a simple prompt to guide its behavior.

```python
from langchain.agents import create_agent
import requests

def get_weather(city: str) -> str:
    """Get real weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url).text

agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant. Use tools when needed.",
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in Bangalore?"}]}
)

print(response["messages"][-1].content)

```

Run:

```python
python3 main.py
```

Expected Output:

```python
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
The weather in Bangalore is 32°C and sunny.
```

# Full Flow (Step-by-step breakdown)

We’ll walk through YOUR exact code and explain what happens at each stage.

---

## STEP 0 — our code setup

```
fromlangchain.agentsimportcreate_agent
importrequests
```

👉 You are using:

- LangChain → agent framework
- `requests` → to call real weather API

---

## STEP 1 — Define the TOOL

```
defget_weather(city:str) ->str:
"""Get real weather for a given city."""
url=f"https://wttr.in/{city}?format=3"
returnrequests.get(url).text
```

### What this does:

- Takes input: `city`
- Calls external API → `wttr.in`
- Returns real weather string

👉 Example:

```
Bangalore: +28°C, Partly cloudy
```

---

### Important Concepts

> 👉 This function = **TOOL**
> 

The LLM **cannot access internet**, so:

- It depends on this function for real-world data

---

## STEP 2 — Create the AGENT

```python
agent=create_agent(
model="google_genai:gemini-2.5-flash",
tools=[get_weather],
system_prompt="You are a helpful assistant. Use tools when needed.",
)
```

---

### What happens internally here

LangChain does 3 things:

---

### 1. Converts your function → Tool schema

```
{
  "name":"get_weather",
  "description":"Get real weather for a given city",
  "parameters": {
    "city":"string"
  }
}
```

---

### 2. Prepares the LLM (from Google)

Model:

```
gemini-2.5-flash
```

It is configured with:

- System prompt
- Tool definitions

---

### 3. Builds an internal workflow (mini LangGraph)

Behind the scenes:

```
User → LLM → Tool → LLM → Final Answer
```

---

## STEP 3 — User sends input

```python
response=agent.invoke(
    {"messages": [{"role":"user","content":"What is the weather in Bangalore?"}]}
)
```

---

## NOW THE REAL FLOW STARTS

---

# Step-by-Step Execution Flow

---

## STEP 4 — Input goes to LLM

LLM receives:

```
System Prompt:
"You are a helpful assistant..."

User:
"What is the weather in Bangalore?"

Tools:
[get_weather]
```

---

## STEP 5 — LLM THINKS (very important)

The model reasons:

> “This is a weather question
> 
> 
> I have a tool called `get_weather`
> 
> I should call it”
> 

---

## STEP 6 — LLM RETURNS TOOL CALL

Instead of answering, it sends:

```
{
  "function_call": {
    "name":"get_weather",
    "arguments": {"city":"Bangalore"}
  }
}
```

---

## STEP 7 — LangChain executes YOUR function

```
get_weather("Bangalore")
```

👉 This runs:

```
requests.get("https://wttr.in/Bangalore?format=3")
```

---

## STEP 8 — External API responds

Example:

```
Bangalore: +28°C, Partly cloudy
```

---

## STEP 9 — Tool result goes back to LLM

Now LLM receives:

```
Tool Output:
"Bangalore: +28°C, Partly cloudy"
```

---

## STEP 10 — LLM generates FINAL answer

It converts raw tool output into a nice response:

```
The current weather in Bangalore is +28°C with partly cloudy conditions.
```

---

## STEP 11 — You print result

```
print(response["messages"][-1].content)
```

👉 You only print **final AI message**

---

# Complete Flow Visual

```
User Question
     ↓
LLM (Gemini)
     ↓ decides
Tool Call → get_weather("Bangalore")
     ↓
External API (wttr.in)
     ↓
Returns weather
     ↓
LLM formats answer
     ↓
Final output to user
```

---

# Useful Insights

---

## 1. LLM doesn’t know Wheather

👉 It only:

- Understands question
- Decides tool usage

---

## 2. TOOL = Source of truth

- If tool is wrong → answer is wrong
- If tool is real → answer is real

---

## 3. LANGCHAIN = Orchestrator

It handles:

- Tool calling
- Message passing
- Execution flow

---

## 4. This is an agent Loop

```
Think → Act → Observe → Respond
```

---

# What you just built

👉 A **tool-using AI agent** with:

- LLM reasoning
- External API integration
- Autonomous decision making

---

# Try these tests

```
What is the weather in Mumbai?
```

👉 Should call tool

---

# Summary

- Sets up LangChain on Ubuntu (Azure VM or local).
- Installs provider packages and uses **Gemini** via `langchain-google-genai`.
- Configures `GEMINI_API_KEY` and `GOOGLE_API_KEY`.
- Builds a basic tool-using agent with a `get_weather(city)` function calling `wttr.in`.
- Explains the full agent loop: user → LLM → tool call → tool result → final answer.