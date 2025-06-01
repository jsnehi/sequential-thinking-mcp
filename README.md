# Sequential Thinking API
A FastAPI-powered sequential thinking framework that combines structured problem-solving methodologies with AI-enhanced analysis. This system helps break down complex problems into manageable, sequential stages while providing intelligent insights at each step
## Overview
Sequential Thinking API is inspired by the Model Context Protocol (MCP) sequential thinking approach, designed to facilitate systematic problem-solving through defined cognitive stages. Unlike scattered, unorganized thinking, this system guides you through a structured process that mirrors how expert problem-solvers approach complex challenges.

*What Makes This Special?*
- *Structured Framework*: Organizes thinking through 5 proven cognitive stages
- *AI-Enhanced*: OpenAI GPT-4 integration provides intelligent analysis and suggestions
- *Progress Tracking*: Visual timeline and comprehensive session management
- *Iterative Process*: Build upon previous thoughts with contextual awareness
- *Persistent Sessions*: Save and revisit complex thinking processes
- *Production Ready*: Built with FastAPI for scalability and performance

## The Sequential Thinking Framework
*The Five Stages*: Our framework follows a proven cognitive methodology:
- Problem Definition    →  Clearly articulate what you're solving
- Research             →  Gather relevant information and context
- Analysis             →  Break down and examine the components
- Synthesis            →  Integrate findings into coherent solutions
- Conclusion           →  Finalize decisions and action plans


*Why This Approach Works*

- *Prevents Analysis Paralysis*: Clear structure keeps you moving forward
- *Reduces Cognitive Bias*: Systematic approach minimizes mental shortcuts
- *Improves Decision Quality*: Thorough process leads to better outcomes
- *Enables Collaboration*: Shared framework facilitates team problem-solving
- *Creates Documentation*: Natural record of reasoning process

## Key Features

- **Core Functionality**
  - *Structured Thinking Sessions*: Create and manage multiple concurrent problem-solving sessions
  - *AI-Powered Analysis*: Each thought receives intelligent analysis and improvement suggestions
  - *Progress Tracking*: Visual timeline showing your journey through the thinking process
  - *Contextual Awareness*: AI considers previous thoughts when analyzing new ones
  - *Metadata Rich*: Track tags, axioms, assumptions, and other thinking artifacts

- **AI Integration**
  - *Thought Analysis*: GPT-4 evaluates each thought's quality and suggests improvements
  - *Next Step Guidance*: AI recommends what to explore next based on your progress
  - *Session Insights*: Comprehensive analysis of your entire thinking process
  - *Bias Detection*: AI helps identify potential blind spots and assumptions
  - *Quality Assessment*: Evaluation of reasoning strength at each stage

- **Management Features**
    - *Timeline Visualization*: See your thought progression chronologically
    - *Summary Generation*: Automatic summaries with stage distribution and insights
    - *Export Capabilities*: JSON export for integration with other tools
    - *Health Monitoring*: Built-in health checks and status monitoring
    - *Session Management*: Create, track, and organize multiple thinking sessions

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Basic understanding of REST APIs

### Installation

Clone the repository
```bash
git clone https://github.com/your-username/sequential-thinking-api.git
cd sequential-thinking-api
```

Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Set environment variables

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Run the application

```bash
python main.py
```
The API will be available at http://localhost:8000/docs


## API Documentation

### Interactive Documentation

#### Once running, visit:
```
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
```
#### Core Endpoints

Add a Thought:
```
POST /sessions/{session_id}/thoughts
```

Add a new thought to your thinking session with AI analysis.

Request Body:
```
json{
    "content": "Your thought content here",
    "thought_number": 1,
    "total_thoughts": 5,
    "stage": "Problem Definition",
    "tags": ["tag1", "tag2"],
    "axioms_used": ["principle1"],
    "assumptions_challenged": ["assumption1"],
    "use_ai_analysis": true
}
```
Get Session Summary
```
GET /sessions/{session_id}/summary
```
Retrieve a comprehensive summary of your thinking session with AI insights.

AI-Guided Next Step
```
POST /sessions/{session_id}/ai-guided-next-step
```

Get AI recommendations for your next thinking step.
Session Management
```
GET /sessions                    # List all sessions
GET /sessions/{id}/thoughts      # Get all thoughts in session
DELETE /sessions/{id}            # Clear session
```
## 💡 Usage Examples

**Business Decision Making**
```python
# Problem Definition
add_thought(
    content="Our customer churn rate is 15% monthly, above industry average of 10%",
    stage="Problem Definition",
    tags=["customer retention", "churn analysis"]
)
```