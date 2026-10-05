"""MCP server exposing a sample dataset of job postings as tools."""
import json
from collections import Counter
from pathlib import Path

from mcp.server.mcpserver import MCPServer

DATA_FILE = Path(__file__).parent / "postings.json"
POSTINGS: list[dict] = json.loads(DATA_FILE.read_text(encoding="utf-8"))

mcp = MCPServer("job-postings")


def _summary(posting: dict) -> dict:
    """Compact view of a posting so the model is not flooded with data."""
    return {
        "id": posting["id"],
        "title": posting["title"],
        "company": posting["company"],
        "location": posting["location"],
        "skills": posting["skills"],
    }


@mcp.tool()
def search_postings_by_skill(skill: str, limit: int = 10) -> list[dict]:
    """Find job postings that ask for a given skill.

    Args:
        skill: One skill name, case-insensitive, for example 'python'.
        limit: Maximum number of postings to return, from 1 to 50.
    """
    skill = skill.strip().lower()
    if not skill:
        raise ValueError("skill must not be empty. Example: 'python'.")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50.")
    hits = [p for p in POSTINGS if skill in [s.lower() for s in p["skills"]]]
    return [_summary(p) for p in hits[:limit]]


@mcp.tool()
def count_postings_by_company(top_n: int = 10) -> dict[str, int]:
    """Count job postings per company, largest first.

    Args:
        top_n: How many companies to return, from 1 to 100.
    """
    if not 1 <= top_n <= 100:
        raise ValueError("top_n must be between 1 and 100.")
    counts = Counter(p["company"] for p in POSTINGS)
    return dict(counts.most_common(top_n))


@mcp.tool()
def get_posting(posting_id: int) -> dict:
    """Get the full record of one posting by its numeric id.

    Args:
        posting_id: The id of the posting, for example 17.
    """
    for p in POSTINGS:
        if p["id"] == posting_id:
            return p
    raise ValueError(
        f"No posting with id {posting_id}. "
        f"Valid ids are 1 to {len(POSTINGS)}."
    )


if __name__ == "__main__":
    mcp.run()
