import uuid
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import Agent

app = FastAPI(
    title="Memory Agent API",
    description="Multi-tenant conversational agent with semantic memory",
    version="1.0.0"
)

# run_id -> Agent instance
_session_cache: Dict[str, Agent] = {}


class InvocationRequest(BaseModel):
    user_id: str = Field(..., description="User identifier for memory isolation")
    run_id: Optional[str] = Field(
        default=None,
        description="Session ID. If omitted, one will be auto-generated."
    )
    query: str = Field(..., description="User message")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata"
    )


class InvocationResponse(BaseModel):
    user_id: str
    run_id: str
    response: str


def _get_or_create_agent(user_id: str, run_id: str) -> Agent:
    """Return cached Agent for this run_id or create a new one."""
    if run_id in _session_cache:
        agent = _session_cache[run_id]

        # Safety check: avoid accidental reuse of same run_id across users
        if agent.user_id != user_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"run_id '{run_id}' is already associated with user "
                    f"'{agent.user_id}', not '{user_id}'"
                )
            )
        return agent

    agent = Agent(user_id=user_id, run_id=run_id)
    _session_cache[run_id] = agent
    return agent


@app.get("/ping")
def ping() -> Dict[str, str]:
    return {
        "status": "ok",
        "message": "Memory Agent API is running"
    }


@app.post("/invocation", response_model=InvocationResponse)
def invocation(req: InvocationRequest) -> InvocationResponse:
    try:
        query = req.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="query cannot be empty")

        run_id = req.run_id or str(uuid.uuid4())[:8]
        agent = _get_or_create_agent(req.user_id, run_id)
        response_text = agent.chat(query)

        return InvocationResponse(
            user_id=req.user_id,
            run_id=run_id,
            response=response_text
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))