import os
import asyncio
from aioconsole import ainput
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from llm_provider import get_llm_provider

# --- Select the LLM you want to use ---
# Example models:
# "openai/gpt-3.5-turbo"
# "anthropic/claude-3-haiku-20240307"
# "cohere/command-r"
SELECTED_MODEL = "openai/gpt-3.5-turbo"


# Define the agent using the provider from llm_provider
litellm_agent = LlmAgent(
    name="litellm_agent",
    model=get_llm_provider(SELECTED_MODEL),
    instruction="You are a helpful assistant.",
    description=f"Answers user questions using LiteLLM with {SELECTED_MODEL}.",
)

async def main():
    """The main asynchronous routine for the agent."""
    print(f"Agent is running with model '{SELECTED_MODEL}'. Type 'exit' to quit.")
    
    session_service = InMemorySessionService()
    session_id = "session-123"
    session_service.create_session(app_name="litellm_app", user_id="user-123", session_id=session_id)

    runner = Runner(
        agent=litellm_agent,
        app_name="litellm_app",
        session_service=session_service
    )

    while True:
        try:
            user_input = await ainput("You: ")
            if user_input.lower() == 'exit':
                break

            content = Content(role='user', parts=[Part(text=user_input)])
            
            final_response = ""
            # Use run_async since we are in an async context
            async for event in runner.run_async(user_id="user-123", session_id=session_id, new_message=content):
                if event.is_final_response() and event.content and event.content.parts:
                    final_response = event.content.parts[0].text
            
            print(f"Agent: {final_response}")
        except (EOFError, KeyboardInterrupt):
            print("\nAgent stopped.")
            break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent stopped.") 