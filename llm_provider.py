import os
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_llm_provider(model: str) -> LiteLlm:
    """
    Returns a LiteLlm instance for the specified model.

    This function checks for the required API keys based on the provider
    in the model string (e.g., 'openai/', 'anthropic/').

    Args:
        model: The model string in LiteLLM format (e.g., "openai/gpt-4o").

    Returns:
        A configured LiteLlm instance.

    Raises:
        RuntimeError: If the required API key for the provider is not found.
    """
    provider = model.split('/')[0]

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY not found in environment variables.")
    elif provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not found in environment variables.")
    elif provider == "cohere":
        if not os.getenv("COHERE_API_KEY"):
            raise RuntimeError("COHERE_API_KEY not found in environment variables.")
    # Add other providers here as needed by checking for their respective API keys.
    
    return LiteLlm(model=model) 