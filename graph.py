from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List, TypedDict, Annotated
import operator
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('webpage_audit_workshop_2.0')

# Set your OpenAI API key
# You can also use environment variables
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Define the state for the graph
class State(TypedDict):
    input: str
    # Use Annotated with operator.add to handle multiple updates in parallel execution
    output: Annotated[List[str], operator.add]

# Define the language model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7
)

# Define node functions
def workshop_supervisor(state: State):
    logger.info("Executing agent node: workshop_supervisor")
    # Process with agent
    prompt = ChatPromptTemplate.from_template("Introduces the audit workflow and manages overall coordination. {input}")
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": [response.content]}

def ads_expert(state: State):
    logger.info("Executing agent node: ads_expert")
    # Process with agent
    prompt = ChatPromptTemplate.from_template("Facebook Ads Audit {input}")
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": [response.content]}

def fb_url_collector(state: State):
    logger.info("Executing tool node: fb_url_collector")
    # Process with tool
    # This is a placeholder for your tool implementation
    return {"output": [f"Tool fb_url_collector processed: {state['input']}"]}

def webpage_url_collector(state: State):
    logger.info("Executing tool node: webpage_url_collector")
    # Process with tool
    # This is a placeholder for your tool implementation
    return {"output": [f"Tool webpage_url_collector processed: {state['input']}"]}

def scraping_tool(state: State):
    logger.info("Executing tool node: scraping_tool")
    # Process with tool
    # This is a placeholder for your tool implementation
    return {"output": [f"Tool scraping_tool processed: {state['input']}"]}

def data_analyzer(state: State):
    logger.info("Executing agent node: data_analyzer")
    # Process with agent
    prompt = ChatPromptTemplate.from_template("Analyzes data from Facebook Ads and scraped content. {input}")
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": [response.content]}

def report_generator(state: State):
    logger.info("Executing agent node: report_generator")
    # Process with agent
    prompt = ChatPromptTemplate.from_template("Compiles audit findings and generates the final report. {input}")
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": [response.content]}

def screenshoot_of_the_ad(state: State):
    logger.info("Executing tool node: screenshoot_of_the_ad")
    # Process with tool
    # This is a placeholder for your tool implementation
    return {"output": [f"Tool screenshoot_of_the_ad processed: {state['input']}"]}

def scraping_of_the_ad(state: State):
    logger.info("Executing tool node: scraping_of_the_ad")
    # Process with tool
    # This is a placeholder for your tool implementation
    return {"output": [f"Tool scraping_of_the_ad processed: {state['input']}"]}

def web_expert(state: State):
    logger.info("Executing agent node: web_expert")
    # Process with agent
    prompt = ChatPromptTemplate.from_template("Web Auditor {input}")
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": [response.content]}

def new_end(state: State):
    logger.info("Executing node: new_end")
    # Process the input
    prompt = ChatPromptTemplate.from_template("Process the following input: {input}")
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": [response.content]}


# Define the workflow graph
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("workshop_supervisor", workshop_supervisor)
workflow.add_node("ads_expert", ads_expert)
workflow.add_node("data_analyzer", data_analyzer)
workflow.add_node("web_expert", web_expert)
workflow.add_node("report_generator", report_generator)

# Define the edges between nodes
workflow.add_edge("workshop_supervisor", "ads_expert")
workflow.add_edge("workshop_supervisor", "data_analyzer")
workflow.add_edge("data_analyzer", "report_generator")
workflow.add_edge("workshop_supervisor", "web_expert")

# Set the entry point
workflow.set_entry_point("workshop_supervisor")

# Compile the graph
app = workflow.compile()

# Main function to run the workflow
def run_workflow(input_text: str):
  logger.info("Starting workflow execution")
  
  # Initialize the state
  initial_state = {"input": input_text}
  
  # Execute the graph
  result = app.invoke(initial_state)
  
  logger.info("Workflow execution completed")
  # For parallel execution, output is a list, so we join the results
  output_data = result.get('output', [])
  return '\n'.join(output_data) if isinstance(output_data, list) else output_data

# Example usage
if __name__ == "__main__":
  user_input = "Hello, I need help with a task."
  output = run_workflow(user_input)
  print(f"Output: {output}")

