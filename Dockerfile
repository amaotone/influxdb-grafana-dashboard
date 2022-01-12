FROM python:3.8.5-slim

WORKDIR /app
RUN pip install "poetry==1.1.6"
COPY pyproject.toml poetry.lock ./
COPY src /app/src
RUN poetry config virtualenvs.in-project true && poetry install --no-dev

CMD ["poetry", "run", "python", "src/main.py"]