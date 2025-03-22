FROM python:3.12-slim

WORKDIR /app

# Copiar os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Instalar o Poetry
RUN pip install poetry

# Instalar as dependências do projeto usando Poetry
RUN poetry install --no-root 

# Copiar o restante do projeto
COPY src/ ./src/

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para executar a aplicação
CMD ["poetry", "run", "streamlit", "run", "src/app.py"]
# CMD ["streamlit", "run", "src/app.py", "--server.address", "0.0.0.0"]