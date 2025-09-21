"""
Hackathon MCP Server for Watson Orchestrate
Deploy on Railway with zero configuration needed!
"""
import asyncio
import json
import os
from mcp.server import Server
from mcp.server.models import InitializationOptions  
import mcp.server.stdio
from mcp.types import *
from duckduckgo_search import DDGS

# Create server instance
server = Server("hackathon-search-mcp")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available search tools for Watson Orchestrate"""
    return [
        Tool(
            name="web_search",
            description="Search the web using DuckDuckGo. Perfect for research, academic searches, and finding current information. Use 'site:sjsu.edu' to search SJSU specifically.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query. Examples: 'machine learning courses site:sjsu.edu', 'AI ethics research', 'Python tutorials'"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results (1-20)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="news_search", 
            description="Search for recent news articles and current events using DuckDuckGo News. Great for finding recent developments in AI, technology, and current affairs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "News search query. Examples: 'AI developments 2025', 'ethical AI news', 'machine learning breakthroughs'"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of articles (1-15)",
                        "default": 8,
                        "minimum": 1, 
                        "maximum": 15
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="academic_search",
            description="Search academic and educational resources. Automatically adds filters for educational sites and academic content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Academic search query. Examples: 'computer science research', 'AI ethics papers', 'machine learning courses'"
                    },
                    "focus": {
                        "type": "string",
                        "enum": ["papers", "courses", "tutorials", "general"],
                        "default": "general",
                        "description": "Type of academic content to focus on"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle search tool execution"""

    try:
        if name == "web_search":
            query = arguments["query"]
            max_results = arguments.get("max_results", 10)

            print(f"🔍 Web search: {query}")

            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return [TextContent(
                    type="text",
                    text=f"No results found for '{query}'. Try rephrasing your search or using different keywords."
                )]

            # Format results for Watson Orchestrate
            formatted_results = [f"**Search Results for: {query}**\n"]

            for i, result in enumerate(results, 1):
                title = result.get('title', 'No Title')[:100]
                url = result.get('href', 'No URL')
                body = result.get('body', 'No description')[:300]

                formatted_results.append(f"""
**{i}. {title}**
🔗 {url}
📝 {body}
""")

            response = "\n".join(formatted_results)
            return [TextContent(type="text", text=response[:4000])]

        elif name == "news_search":
            query = arguments["query"] 
            max_results = arguments.get("max_results", 8)

            print(f"📰 News search: {query}")

            with DDGS() as ddgs:
                news_results = list(ddgs.news(query, max_results=max_results))

            if not news_results:
                return [TextContent(
                    type="text",
                    text=f"No recent news found for '{query}'. Try different keywords or check spelling."
                )]

            formatted_news = [f"**Recent News: {query}**\n"]

            for i, article in enumerate(news_results, 1):
                title = article.get('title', 'No Title')[:120]
                url = article.get('url', 'No URL')
                source = article.get('source', 'Unknown Source')
                date = article.get('date', 'No Date')
                body = article.get('body', 'No summary')[:250]

                formatted_news.append(f"""
**{i}. {title}**
📰 {source} | 📅 {date}
🔗 {url}  
📄 {body}
""")

            response = "\n".join(formatted_news)
            return [TextContent(type="text", text=response[:4000])]

        elif name == "academic_search":
            query = arguments["query"]
            focus = arguments.get("focus", "general")

            print(f"🎓 Academic search: {query} (focus: {focus})")

            # Add academic filters based on focus
            academic_query = query
            if focus == "papers":
                academic_query += " site:arxiv.org OR site:scholar.google.com OR filetype:pdf"
            elif focus == "courses": 
                academic_query += " site:edu course OR curriculum OR syllabus"
            elif focus == "tutorials":
                academic_query += " tutorial OR guide OR how-to site:edu"
            else:
                academic_query += " site:edu OR site:arxiv.org"

            with DDGS() as ddgs:
                results = list(ddgs.text(academic_query, max_results=10))

            if not results:
                return [TextContent(
                    type="text", 
                    text=f"No academic results found for '{query}'. Try broader terms or different focus area."
                )]

            formatted_results = [f"**Academic Search: {query}** (Focus: {focus})\n"]

            for i, result in enumerate(results, 1):
                title = result.get('title', 'No Title')[:100]
                url = result.get('href', 'No URL')
                body = result.get('body', 'No description')[:300]

                # Try to identify the type of academic content
                content_type = "📄 Resource"
                if "arxiv.org" in url:
                    content_type = "📊 Paper"
                elif "course" in title.lower() or "syllabus" in body.lower():
                    content_type = "📚 Course"
                elif "tutorial" in title.lower() or "guide" in title.lower():
                    content_type = "🎯 Tutorial"

                formatted_results.append(f"""
**{i}. {title}**
{content_type} | 🔗 {url}
📝 {body}
""")

            response = "\n".join(formatted_results)
            return [TextContent(type="text", text=response[:4000])]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}. Available tools: web_search, news_search, academic_search"
            )]

    except Exception as e:
        print(f"❌ Error in {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Search temporarily unavailable. Please try again in a moment. Error: {str(e)[:100]}"
        )]

async def main():
    """Start the MCP server"""
    print("🚀 Starting Hackathon MCP Server...")
    print("🎯 Ready for Watson Orchestrate integration!")
    print("🔍 Available tools: web_search, news_search, academic_search")

    async with mcp.server.stdio.stdio_server() as streams:
        await server.run(streams[0], streams[1])

if __name__ == "__main__":
    # Set up environment for Railway
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Server will run on port {port}")
    asyncio.run(main())
