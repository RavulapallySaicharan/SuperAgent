from openai import OpenAI
from fastmcp import FastMCP
import re

client = OpenAI(
    api_key=""""""
)

# Create an MCP server
# Specify dependencies for deployment and development
mcp = FastMCP("Python Code Search🚀", dependencies=["openai"])


# Include web search results for the completion
@mcp.tool()
def search_python_code(query: str):
    """Searches for Python code examples based on a user's query and extracts the code.
    The query should describe what Python code you're looking for,
    such as "how to read CSV files in Python" or "Python web scraping with requests".
    Returns the extracted Python code examples from web search results.
    """
    # Modify the query to specifically search for Python code examples
    search_query = f"Python code example: {query}"
    
    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        web_search_options={},
        messages=[
            {
                "role": "user",
                "content": f"Search for Python code examples related to: {query}. Please provide complete, working Python code snippets with explanations. Focus on practical, runnable code examples.",
            }
        ],
    )
    
    # Extract the response
    response = completion.choices[0].message.content
    
    # Try to extract Python code blocks from the response
    python_code_blocks = extract_python_code(response)
    
    if python_code_blocks:
        return {
            "query": query,
            "code_blocks": python_code_blocks,
            "full_response": response
        }
    else:
        return {
            "query": query,
            "code_blocks": [],
            "full_response": response,
            "message": "No Python code blocks found in the search results"
        }


def extract_python_code(text: str) -> list:
    """Extract Python code blocks from text using regex patterns"""
    code_blocks = []
    
    # Pattern to match code blocks with ```python or ```py
    python_block_pattern = r'```(?:python|py)\s*\n(.*?)\n```'
    matches = re.findall(python_block_pattern, text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        if match.strip():
            code_blocks.append(match.strip())
    
    # Pattern to match code blocks with just ```
    generic_block_pattern = r'```\s*\n(.*?)\n```'
    matches = re.findall(generic_block_pattern, text, re.DOTALL)
    
    for match in matches:
        # Check if the content looks like Python code
        if is_python_code(match.strip()):
            code_blocks.append(match.strip())
    
    # Pattern to match indented code blocks (common in documentation)
    indented_pattern = r'(?:^|\n)(\s+(?:def|class|import|from|if|for|while|try|with|async def)\s+.*?)(?=\n\S|\Z)'
    matches = re.findall(indented_pattern, text, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        if is_python_code(match.strip()):
            code_blocks.append(match.strip())
    
    return list(set(code_blocks))  # Remove duplicates


def is_python_code(text: str) -> bool:
    """Check if text looks like Python code"""
    python_keywords = [
        'def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ', 
        'try:', 'except:', 'finally:', 'with ', 'async def', 'await ',
        'return ', 'yield ', 'raise ', 'assert ', 'pass', 'break', 'continue',
        'print(', 'len(', 'range(', 'list(', 'dict(', 'set(', 'tuple(',
        'True', 'False', 'None', 'self.', '__init__', 'super('
    ]
    
    # Count Python keywords in the text
    keyword_count = sum(1 for keyword in python_keywords if keyword in text)
    
    # Check for Python syntax patterns
    has_python_syntax = (
        ':' in text and  # Colons for blocks
        ('def ' in text or 'class ' in text or 'if ' in text or 'for ' in text) and
        keyword_count >= 2  # At least 2 Python keywords
    )
    
    return has_python_syntax


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    completion = client.chat.completions.create(
        model="gpt-4o-search-preview",
        web_search_options={},
        messages=[
            {
                "role": "user",
                "content": f"What is the weather forecast for this week in {city}?",
            }
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    mcp.run(transport="stdio")