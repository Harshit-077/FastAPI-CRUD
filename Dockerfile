FROM python:3.12-slim

WORKDIR /app

# Install uv

RUN pip install --no-cache-dir uv

# Copy dependency files first for better layer caching

COPY pyproject.toml uv.lock ./

# Install project dependencies

RUN uv sync --frozen --no-dev

# Copy application code

COPY main.py ./

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
