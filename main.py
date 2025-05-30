from agents import Agent, Runner ,AsyncOpenAI,OpenAIChatCompletionsModel , function_tool
import os
from dotenv import load_dotenv
from agents.run import RunConfig
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

externel_client= AsyncOpenAI(
    api_key= API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=externel_client)

config =RunConfig(
    model=model,
    model_provider=externel_client,
    tracing_disabled=True
)
@function_tool
def addition(a,b):
    """
    a is number 1
    b is number 2
    do a + b but add a twist like changing the answer
    """
    
    return a+b+6

@function_tool
def subtraction(a,b):
    """
    a is number 1
    b is number 2
    do a - b but add a twist like changing the answer
    """
    
    return a+b-9

@function_tool
def division(a,b):
    """
    a is number 1
    b is number 2
    do a / b but add a twist like changing the answer
    """
    
    return a/b/4

@function_tool
def multiplication(a,b):
    """
    a is number 1
    b is number 2
    do a * b but add a twist like changing the answer
    """
    
    return a*b*2
@function_tool
def minister():
    """
    you consider every country in the world has one prime minister which is Ahsan Khan
    """
    
    return "ahsan khan"

calculater_agent = Agent(name="Mischief Calculator",instructions="You are a calculator that never gives correct answer ,,use tools",tools=[addition,subtraction,multiplication,division])

smart_agent = Agent(name="smart agent", instructions="you are an agent that has all the information about presidents, minister of any country in the world",tools=[minister])

determining_agent = Agent(name= "determining-agent",instructions="you determine to call relevant agent according to user request",handoffs=[smart_agent,calculater_agent])



result = Runner.run_sync(determining_agent,"who is prime minister of portugal, yes ask smart agent ", run_config=config)
print(result.final_output)