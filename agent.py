from customs_tools.tools import UtilityTools
from llms.llm import LLMModel
from prompts.prompt import SYSTEM_PROMPT

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState,StateGraph, END, START
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition


class TravelAgent:
    def __init__(self):
        llm_model = LLMModel()
        custom_tool = UtilityTools()
        self.tools=[custom_tool.currency_converter, custom_tool.weather_forecast, TavilySearchResults()]
        self.llm_model=llm_model.get_model()
        self.llm_with_tools = self.llm_model.bind_tools(self.tools)

    def supervisor_node(self, state:MessagesState):
        user_question=state["messages"]
        input_question = [SYSTEM_PROMPT]+user_question
        response = self.llm_with_tools.invoke(input_question)
        return {
            "messages":[response]
        }
    
    def workflow(self):
        self.graph = StateGraph(MessagesState)
        self.graph.add_node("llm_decision_step",self.supervisor_node)
        self.graph.add_node("tools",ToolNode(self.tools))
        self.graph.add_edge(START,"llm_decision_step")
        self.graph.add_conditional_edges("llm_decision_step",tools_condition)
        self.graph.add_edge("tools","llm_decision_step")
        self.app = self.graph.compile()
        return self.app

    