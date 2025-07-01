FROM python:3.10-slim

WORKDIR /app

COPY planner_agent.py .
COPY solver_agent.py .

# Install correct packages
RUN pip install --no-cache-dir openai requests

# Run everything at runtime using CMD (not at build time)
CMD ["sh", "-c", "python planner_agent.py && python solver_agent.py && python solve_ctf.py"]