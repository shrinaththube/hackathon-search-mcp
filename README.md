# 🚀 Hackathon MCP Server - Watson Orchestrate Search

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy?template=https://github.com/YOUR_USERNAME/hackathon-mcp-server)

**🎯 Purpose**: Get hackathon students building AI agents in 5 minutes, not 5 hours!

## 🎓 FOR STUDENTS: Quick Deploy Guide

### **Step 1: Fork This Repository (30 seconds)**
1. **Click the "Fork" button** at the top of this page
2. **Keep the default settings** and click "Create fork"
3. **You now have your own copy** of the code!

### **Step 2: Deploy to Railway (2 minutes)**
1. **Click this button**: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy)
2. **Sign up with GitHub** (Railway will ask for GitHub access)
3. **Select your forked repository** from the list
4. **Click "Deploy Now"** and wait 2-3 minutes
5. **Copy your URL** from Railway dashboard (looks like: `https://your-app-name-production.railway.app`)

### **Step 3: Connect to Watson Orchestrate (2 minutes)**
1. **Go to**: `https://watsonx-orchestrate.ibm.com`
2. **Create agent** → **Add tool** → **Add from MCP server**
3. **Enter your Railway URL** from Step 2
4. **Import tools**: Select all 3 search tools
5. **Test**: Try "Search for AI ethics research"

🎉 **DONE!** You now have a personal AI research agent!

---

## 🔧 **What You Get**

✅ **Web Search** - Search any topic on the internet  
✅ **News Search** - Find recent articles and developments  
✅ **Academic Search** - Research papers, courses, tutorials  
✅ **SJSU Specific** - Use `site:sjsu.edu` for campus info  
✅ **Your Own Server** - No sharing, full control  
✅ **Free Hosting** - Railway's free tier covers hackathon usage  

---

## 💡 **Project Ideas Using Your Search Agent**

### 🎓 **SJSU Study Buddy**
Help students navigate academics and campus life
```
Search for computer science degree requirements site:sjsu.edu
Find SJSU library study spaces and hours
Search for professor ratings and course reviews
```

### 📚 **Research Assistant** 
Ethical AI research and academic support
```
Search for recent papers on AI bias and fairness
Find machine learning datasets for projects  
Search for AI ethics guidelines and frameworks
```

### 🏫 **Campus Concierge**
Student services and campus information
```
Find SJSU dining options and hours
Search for campus events and activities
Find parking information and transportation
```

### 💼 **Career Helper**
Job search and professional development
```
Search for software engineering internships Bay Area
Find resume templates for computer science students
Search for coding interview preparation resources
```

---

## 🛠 **Technical Details**

- **Language**: Python 3.11
- **Framework**: MCP (Model Context Protocol)
- **Search Engine**: DuckDuckGo (no API keys needed!)
- **Hosting**: Railway.app (free tier)
- **Watson Orchestrate**: Compatible MCP server

---

## 🔍 **Available Search Tools**

### **1. Web Search (`web_search`)**
- Search any topic on the internet
- Use `site:domain.com` for specific sites
- Perfect for general research and information

### **2. News Search (`news_search`)**  
- Find recent news articles and current events
- Great for staying updated on AI/tech developments
- Includes source and date information

### **3. Academic Search (`academic_search`)**
- Automatically filters for educational content
- Focus options: papers, courses, tutorials, general
- Searches .edu sites, arXiv, and academic resources

---

## ⚠️ **Troubleshooting**

### **Railway Deployment Issues:**
- **Build Failed**: Check that you forked the repo correctly
- **App Crashed**: Wait 2-3 minutes, Railway auto-restarts
- **No URL**: Go to Railway dashboard → Settings → Generate Domain

### **Watson Orchestrate Issues:**
- **MCP Server Won't Connect**: Make sure Railway app is running (green status)
- **Tools Won't Import**: Try entering the URL again, check for typos
- **Search Not Working**: Test your Railway URL in a browser first

### **Search Quality Issues:**
- **Bad Results**: Be more specific in your queries
- **No SJSU Results**: Add `site:sjsu.edu` to your search
- **Need Recent Info**: Use the news_search tool instead

---

## 🎯 **Success Tips**

1. **Test your deployment** before the hackathon starts
2. **Bookmark your Railway dashboard** for easy access
3. **Try different search tools** to see which works best for your project
4. **Use specific search terms** rather than general ones
5. **Combine searches** to get comprehensive information

---

## 🆘 **Need Help?**

- **Slack**: #hackathon-help channel
- **Issues**: [Create an issue](https://github.com/YOUR_USERNAME/hackathon-mcp-server/issues) on this repo
- **TA Hours**: Check schedule for in-person help
- **Peer Support**: Ask your teammates!

---

## 📊 **What Makes This Special**

- **5-minute setup** instead of hours debugging APIs
- **Your own server** - no sharing or rate limits  
- **No API keys** - no credit cards or account management
- **Production ready** - real search results, not mock data
- **Educational focus** - optimized for student research needs

---

**Built for SJSU Computer Science hackathons** 🎓  
**Focus on innovation, not infrastructure!** 🚀

---

## 🔄 **Advanced: Customizing Your Server**

Want to modify the search functionality? Edit `server.py`:

```python
# Add custom search filters
academic_query += " site:sjsu.edu OR site:github.com"

# Modify result formatting  
formatted_results.append(f"**{title}** - {url}")

# Add new search tools
# Follow the existing pattern in the code
```

After editing, Railway will auto-deploy your changes!
