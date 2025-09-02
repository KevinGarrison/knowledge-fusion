from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from tools.internal.google_mcp_toolbox import GoogleMCPtoolbox
from typing import Literal
from langgraph.graph import END, START
from langchain_core.messages import HumanMessage, SystemMessage


def main():
    # Define the function that calls the model
    def call_model(state: MessagesState):
        messages = state['messages']
        response = tool_llm.invoke(messages)
        return {"messages": [response]}  # Return a list to add to existing messages

    # Define the function that determines whether to continue or not
    def should_continue(state: MessagesState) -> Literal["tools", END]:
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"  # Route to "tools" node if LLM makes a tool call
        return END  # Otherwise, stop
    
    with GoogleMCPtoolbox() as toolbox:
        model = ChatOpenAI(model='gpt-5')
        tool_llm = model.bind_tools(toolbox.tools)
        builder = StateGraph(MessagesState)
        tool_node = ToolNode(tools=toolbox.tools)

        builder.add_node("agent", call_model)
        builder.add_node("tools", tool_node)

        builder.add_edge(START, "agent")
        builder.add_conditional_edges("agent", should_continue)
        builder.add_edge("tools", 'agent')

        graph = builder.compile()

        result = graph.invoke({
            "messages": [
                SystemMessage(content="You can call tools. When manipulating Redis, always use the appropriate tool."),
                HumanMessage(content="Use the tool manage-users to get a user with id 2, output it and then delete it based on the id without confirmation.")
            ]
        })
        final_message = result["messages"][-1]
        print(final_message.content)

if __name__ == "__main__":
    main()
