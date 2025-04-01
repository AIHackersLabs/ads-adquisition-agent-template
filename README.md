# Ads Acquisition Agent

This project is a LangGraph-based template designed to audit Meta ads and webpage content to provide insights on ad performance and compliance.

## Features

- Meta Ads auditing
- Webpage content analysis
- Data analysis of collected information
- Automated report generation
- Multi-agent collaboration with specialized experts

## Project Structure

The application is built using LangGraph, a framework for building stateful, multi-agent workflows. It includes:

- Multiple specialized agents (Workshop Supervisor, Ads Expert, Web Expert, Data Analyzer)
- Tool nodes for data collection and processing
- A configurable workflow graph that coordinates the agents

## Requirements

- Python 3.11+
- LangGraph
- LangChain
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AIHackersLabs/ads-adquisition-agent-template
cd ads-adquisition-agent-template
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your-openai-api-key
LANGSMITH_API_KEY=your-langsmith-api-key  # Optional, for tracing
LANGCHAIN_TRACING_V2=true  # Optional, for tracing
LANGSMITH_PROJECT=your-project-name  # Optional, for tracing
```

## Running the Application

To run the application locally with LangGraph dev server:

```bash
langgraph dev
```

This will start the LangGraph server.

### Using the API

You can interact with the application using the LangGraph SDK:

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:2024")

async for chunk in client.runs.stream(
    None,  # Threadless run
    "agent",  # Name of assistant. Defined in langgraph.json
    input={
        "messages": [{
            "role": "human",
            "content": "Audit this Meta ad: <URL>",
        }],
    },
    stream_mode="updates",
):
    print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    print("\n\n")
```

## Customization

To customize the workflow:

1. Modify `graph.py` to add new agents or tools
2. Update the graph structure by modifying the edges between nodes
3. Implement your own custom tools by updating the tool node functions

## License

This project is licensed under the MIT License. See the LICENSE file for more details.