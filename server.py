"""
Hackathon MCP Server for Watson Orchestrate
Railway-compatible HTTP server with search capabilities
"""
import asyncio
import json
import os
from typing import Any, Dict, List
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from duckduckgo_search import DDGS

# FastAPI app for Railway HTTP deployment
app = FastAPI(
    title="Hackathon MCP Server",
    description="Search capabilities for Watson Orchestrate hackathons",
    version="1.0.0"
)

# Request/Response models
class SearchRequest(BaseModel):
    query: str
    max_results: int = 10

class NewsRequest(BaseModel):
    query: str
    max_results: int = 8

class AcademicRequest(BaseModel):
    query: str
    focus: str = "general"
    max_results: int = 10

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
    query: str

@app.get("/")
async def root():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "service": "Hackathon MCP Search Server", 
        "version": "1.0.0",
        "available_endpoints": [
            "/search - Web search",
            "/news - News search", 
            "/academic - Academic search",
            "/health - Health check"
        ]
    }

@app.get("/health")
async def health_check():
    """Railway health check endpoint"""
    return {"status": "ok", "service": "running"}

@app.post("/search", response_model=SearchResponse)
async def web_search(request: SearchRequest):
    """Web search using DuckDuckGo"""
    try:
        print(f"🔍 Web search: {request.query}")

        with DDGS() as ddgs:
            results = list(ddgs.text(request.query, max_results=request.max_results))

        if not results:
            return SearchResponse(
                results=[],
                total=0,
                query=request.query
            )

        # Format results
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append({
                "rank": i,
                "title": result.get('title', 'No Title')[:150],
                "url": result.get('href', 'No URL'),
                "description": result.get('body', 'No description')[:400],
                "type": "web"
            })

        return SearchResponse(
            results=formatted_results,
            total=len(formatted_results),
            query=request.query
        )

    except Exception as e:
        print(f"❌ Web search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.post("/news", response_model=SearchResponse)
async def news_search(request: NewsRequest):
    """News search using DuckDuckGo News"""
    try:
        print(f"📰 News search: {request.query}")

        with DDGS() as ddgs:
            news_results = list(ddgs.news(request.query, max_results=request.max_results))

        if not news_results:
            return SearchResponse(
                results=[],
                total=0,
                query=request.query
            )

        # Format news results
        formatted_results = []
        for i, article in enumerate(news_results, 1):
            formatted_results.append({
                "rank": i,
                "title": article.get('title', 'No Title')[:150],
                "url": article.get('url', 'No URL'),
                "description": article.get('body', 'No summary')[:400],
                "source": article.get('source', 'Unknown Source'),
                "date": article.get('date', 'No Date'),
                "type": "news"
            })

        return SearchResponse(
            results=formatted_results,
            total=len(formatted_results),
            query=request.query
        )

    except Exception as e:
        print(f"❌ News search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"News search error: {str(e)}")

@app.post("/academic", response_model=SearchResponse)
async def academic_search(request: AcademicRequest):
    """Academic search with educational filters"""
    try:
        print(f"🎓 Academic search: {request.query} (focus: {request.focus})")

        # Add academic filters based on focus
        academic_query = request.query
        if request.focus == "papers":
            academic_query += " site:arxiv.org OR site:scholar.google.com OR filetype:pdf"
        elif request.focus == "courses":
            academic_query += " site:edu course OR curriculum OR syllabus"
        elif request.focus == "tutorials":
            academic_query += " tutorial OR guide OR how-to site:edu"
        else:
            academic_query += " site:edu OR site:arxiv.org"

        with DDGS() as ddgs:
            results = list(ddgs.text(academic_query, max_results=request.max_results))

        if not results:
            return SearchResponse(
                results=[],
                total=0,
                query=request.query
            )

        # Format academic results with content type detection
        formatted_results = []
        for i, result in enumerate(results, 1):
            url = result.get('href', 'No URL')
            title = result.get('title', 'No Title')

            # Detect academic content type
            content_type = "resource"
            if "arxiv.org" in url:
                content_type = "paper"
            elif "course" in title.lower() or "syllabus" in result.get('body', '').lower():
                content_type = "course"
            elif "tutorial" in title.lower() or "guide" in title.lower():
                content_type = "tutorial"

            formatted_results.append({
                "rank": i,
                "title": title[:150],
                "url": url,
                "description": result.get('body', 'No description')[:400],
                "content_type": content_type,
                "focus": request.focus,
                "type": "academic"
            })

        return SearchResponse(
            results=formatted_results,
            total=len(formatted_results),
            query=request.query
        )

    except Exception as e:
        print(f"❌ Academic search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Academic search error: {str(e)}")

# Watson Orchestrate compatible endpoints
@app.get("/mcp/capabilities")
async def mcp_capabilities():
    """MCP server capabilities for Watson Orchestrate"""
    return {
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "hackathon-search-server",
            "version": "1.0.0"
        },
        "tools": [
            {
                "name": "web_search",
                "description": "Search the web using DuckDuckGo. Perfect for research and finding current information.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Number of results (1-20)",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "news_search",
                "description": "Search for recent news articles and current events",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "News search query"
                        },
                        "max_results": {
                            "type": "integer", 
                            "description": "Number of articles (1-15)",
                            "default": 8
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "academic_search",
                "description": "Search academic and educational resources",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Academic search query"
                        },
                        "focus": {
                            "type": "string",
                            "enum": ["papers", "courses", "tutorials", "general"],
                            "default": "general"
                        },
                        "max_results": {
                            "type": "integer",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    }

@app.post("/mcp/call_tool")
async def mcp_call_tool(request: dict):
    """MCP tool execution endpoint for Watson Orchestrate"""
    tool_name = request.get("name")
    arguments = request.get("arguments", {})

    try:
        if tool_name == "web_search":
            search_req = SearchRequest(**arguments)
            result = await web_search(search_req)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": format_search_results(result)
                    }
                ]
            }
        elif tool_name == "news_search":
            news_req = NewsRequest(**arguments) 
            result = await news_search(news_req)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": format_news_results(result)
                    }
                ]
            }
        elif tool_name == "academic_search":
            academic_req = AcademicRequest(**arguments)
            result = await academic_search(academic_req)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": format_academic_results(result)
                    }
                ]
            }
        else:
            return {
                "error": f"Unknown tool: {tool_name}",
                "available_tools": ["web_search", "news_search", "academic_search"]
            }
    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}"
        }

def format_search_results(response: SearchResponse) -> str:
    """Format search results for Watson Orchestrate"""
    if not response.results:
        return f"No results found for '{response.query}'. Try different keywords."

    formatted = [f"**Search Results for: {response.query}** ({response.total} results)\n"]

    for result in response.results[:10]:  # Limit to top 10
        formatted.append(f"""
**{result['rank']}. {result['title']}**
🔗 {result['url']}
📝 {result['description']}
""")

    return "\n".join(formatted)

def format_news_results(response: SearchResponse) -> str:
    """Format news results for Watson Orchestrate"""
    if not response.results:
        return f"No recent news found for '{response.query}'. Try different keywords."

    formatted = [f"**Recent News: {response.query}** ({response.total} articles)\n"]

    for result in response.results:
        formatted.append(f"""
**{result['rank']}. {result['title']}**
📰 {result.get('source', 'Unknown')} | 📅 {result.get('date', 'No date')}
🔗 {result['url']}
📄 {result['description']}
""")

    return "\n".join(formatted)

def format_academic_results(response: SearchResponse) -> str:
    """Format academic results for Watson Orchestrate"""
    if not response.results:
        return f"No academic results found for '{response.query}'. Try broader terms."

    focus = response.results[0].get('focus', 'general') if response.results else 'general'
    formatted = [f"**Academic Search: {response.query}** (Focus: {focus}, {response.total} results)\n"]

    for result in response.results:
        content_type_icon = {
            "paper": "📊",
            "course": "📚", 
            "tutorial": "🎯",
            "resource": "📄"
        }.get(result.get('content_type', 'resource'), '📄')

        formatted.append(f"""
**{result['rank']}. {result['title']}**
{content_type_icon} {result.get('content_type', 'Resource').title()} | 🔗 {result['url']}
📝 {result['description']}
""")

    return "\n".join(formatted)

if __name__ == "__main__":
    # Railway deployment configuration
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting Hackathon Search Server on port {port}")
    print("🎯 Endpoints: /search, /news, /academic, /mcp/capabilities")
    print("🔍 Ready for Watson Orchestrate and direct HTTP requests!")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
