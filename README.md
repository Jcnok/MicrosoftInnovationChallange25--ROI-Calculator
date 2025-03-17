# Start Project Template

## Requisitos

- Python 3.12
- Poetry

## Como usar

### 1. Instale as dependências

```bash
poetry install
```

### 2. Rodar os comandos de formatação e linting

```bash
poetry run task format
```

### 3. Rodar os testes

```bash
poetry run pytest
```

## Estrutura do Projeto

- `src/`: Código fonte do projeto
- `tests/`: Testes automatizados

## Integração Contínua (CI)

Este projeto utiliza GitHub Actions para Integração Contínua (CI). A configuração do CI está definida no arquivo `.github/workflows/python-ci.yml`, que automatiza o processo de teste e verificação de código. Abaixo estão os detalhes sobre como o CI foi configurado:

### 1. Configuração do CI

O arquivo `.github/workflows/python-ci.yml` define um workflow que executa automaticamente o pipeline de CI para cada push para a branch `main` e para cada pull request. O workflow inclui os seguintes passos:

- **Verificação de Código**: Usa ferramentas de formatação e linting (`isort`, `black`, `flake8`) para garantir que o código esteja bem formatado e siga as melhores práticas.
- **Execução de Testes**: Executa os testes automatizados com `pytest` para garantir que o código esteja funcionando conforme o esperado.

### 2. Como Funciona

- **Push para a Branch `main`**: Sempre que você faz um push para a branch `main`, o GitHub Actions executa o pipeline de CI definido no arquivo `python-ci.yml`. Isso inclui a instalação das dependências, formatação e linting do código, e a execução dos testes.
- **Pull Requests**: Sempre que um pull request é criado ou atualizado, o pipeline de CI é executado para garantir que as mudanças propostas não quebrem o código existente e estejam em conformidade com as regras de formatação e linting.

### 3. Arquivo de Workflow CI

Aqui está a configuração do workflow para referência:

```yaml
name: Python CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12  # Atualize para a versão atual do Python que você está usando

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run Linting
        run: |
          poetry run task format

      - name: List installed packages
        run: |
          poetry show

      - name: Run Tests
        run: |
          poetry run pytest
```

### 4. Como Replicar a Configuração

Para replicar esta configuração de CI em outro projeto, siga estes passos:

1. **Crie o Arquivo de Workflow**:
  - No repositório do seu projeto, crie um diretório `.github/workflows/` se ainda não existir.
  - Adicione um arquivo chamado `python-ci.yml` dentro deste diretório.

2. **Adicione a Configuração ao Arquivo de Workflow**:
  - Copie e cole a configuração YAML fornecida acima no arquivo `python-ci.yml`.

3. **Configuração do Projeto**:
  - Certifique-se de que o seu projeto utiliza `poetry` e que os comandos de formatação, linting e testes estão configurados corretamente no seu `pyproject.toml`.

4. **Commit e Push**:
  - Faça um commit e push das alterações para o repositório remoto. O GitHub Actions começará a executar o pipeline automaticamente com base na configuração fornecida..
