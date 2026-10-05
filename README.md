# Job Postings MCP Server

A small Model Context Protocol (MCP) server, built with the official MCP Python SDK
(FastMCP), that lets an AI assistant query a sample dataset of job postings.

## Dataset
`postings.json` holds 120 **synthetic** postings made by `generate_data.py`
(fictional companies, random skills). It is not real market data.

## Tools
| Tool | Inputs | What it does |
|---|---|---|
| `search_postings_by_skill` | `skill: str`, `limit: int = 10` (1 to 50) | Returns compact summaries of postings that list the skill |
| `count_postings_by_company` | `top_n: int = 10` (1 to 100) | Returns posting counts per company, largest first |
| `get_posting` | `posting_id: int` | Returns one full posting, or an error that names the valid id range |

Bad input (empty skill, limit out of range, unknown id) raises an error with a message
that says what to fix.

## Run it
```bash
python -m venv venv && source venv/bin/activate
pip install "mcp[cli]"
python generate_data.py
mcp dev server.py       
```

## Proof it works
TODO: add a screenshot of the MCP Inspector (or an AI assistant) calling each tool.

## How I would protect this server with OAuth 2.0
This is a design, not implemented code.

- **Flow:** authorization code flow with PKCE, so a client (an AI assistant) gets a token
  on behalf of a signed-in user without handling the user's password.
- **Roles:** the server is the resource server. A separate authorization server signs the user in
  and issues tokens.
- **Where tokens are checked:** on every request to the server, before any tool runs. Check the
  signature, expiry, audience (the token was issued for this server) and scopes.
- **Scopes:** `postings:read` for search and get, `postings:stats` for the counts. A client gets
  only what it asks for and the user approves.
- **Tokens:** short-lived access tokens, with refresh tokens kept by the client and revocable.
- **Also:** rate limiting, logging of who called which tool, no secrets in the repo.

TODO: check this against the current MCP authorization specification before submitting.

## Limits and what I would improve next
- The data is synthetic and small, so results say nothing about the real job market.
- Search matches exact skill names only (no synonyms).
- The server uses stdio only and has no authentication yet.
- Next: run it over HTTP with token checks, load a real dataset, add tests.

## Rust (stretch)
`rust-reader/` is a small Rust program that reads the same `postings.json` and prints
postings per company: `cd rust-reader && cargo run`.
