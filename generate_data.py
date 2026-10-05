"""Generate a SYNTHETIC sample of job postings. This is not real data."""
import json
import random

random.seed(42)

COMPANIES = ["Acme Analytics", "Baobab Tech", "Cobalt Labs", "Delta Health",
             "Everest Data", "Fig Systems", "Giraffe Pay", "Harvest AI"]
TITLES = ["Backend Engineer", "Data Analyst", "ML Engineer",
          "Frontend Developer", "DevOps Engineer", "Security Engineer"]
LOCATIONS = ["Nairobi", "Remote", "Lagos", "Kigali", "Accra", "Addis Ababa"]
SKILLS = ["python", "sql", "fastapi", "react", "docker", "aws",
          "typescript", "rust", "go", "pandas", "oauth", "git"]


def make_posting(posting_id: int) -> dict:
    return {
        "id": posting_id,
        "title": random.choice(TITLES),
        "company": random.choice(COMPANIES),
        "location": random.choice(LOCATIONS),
        "date": f"2026-09-{random.randint(1, 30):02d}",
        "skills": random.sample(SKILLS, k=random.randint(3, 5)),
    }


if __name__ == "__main__":
    postings = [make_posting(i) for i in range(1, 121)]
    with open("postings.json", "w", encoding="utf-8") as f:
        json.dump(postings, f, indent=2)
    print(f"Wrote {len(postings)} synthetic postings to postings.json")
