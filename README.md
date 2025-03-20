<div align="center">
  <h1>ROI Vision: Análise Inteligente de Projetos</h1>
  <p>Uma ferramenta inteligente para análise e comparação de projetos utilizando IA.</p>
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-1.39.0+-red.svg" alt="Streamlit Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
  <img src="https://img.shields.io/badge/Azure%20OpenAI-blueviolet.svg" alt="Azure OpenAI">  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">
</div>

##  Estrutura do Projeto

```bash
roi_vision/
├── img/                       # Imagens do projeto
├── teste/                     # Testes com pytest
├── src/                       # Código fonte
│   └── app.py                 # Aplicação principal
├── .env.example               # Exemplo de variáveis de ambiente
├── .flake8                    # Configuração do flake8
├── .gitignore                 # Arquivos ignorados pelo Git
├── .pre-commit-config.yaml    # Configuração do pre-commit
├── .python-version            # Versão do Python utilizada
├── LICENSE                    # Licença do projeto
├── poetry.lock                # Lockfile do Poetry
├── pyproject.toml             # Configuração do Poetry
└── README.md                  # Este arquivo
```
##  Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Índice](#índice)
- [Sobre o Projeto](#sobre-o-projeto)
  - [Calculadora de ROI Comparativa com IA](#calculadora-de-roi-comparativa-com-ia)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos](#requisitos)
- [⚙️ Instalação e Execução](#️-instalação-e-execução)
  - [Execução Local com Poetry](#execução-local-com-poetry)
- [Conclusão e Aprendizados](#conclusão-e-aprendizados)
  - [Próximos Passos:](#próximos-passos)

##  Sobre o Projeto

[ Voltar ao índice](#-índice)

"ROI Vision: Análise Inteligente de Projetos" é uma aplicação web desenvolvida para o Hackathon da Microsoft, que utiliza inteligência artificial para calcular e comparar KPIs financeiros de projetos. A ferramenta visa auxiliar na tomada de decisões estratégicas, fornecendo insights valiosos e recomendações acionáveis.

###  Calculadora de ROI Comparativa com IA

[ Voltar ao índice](#-índice)

A calculadora utiliza a API Azure OpenAI GPT-4o mini para analisar dados de projetos e calcular KPIs como ROI e VPL. Características principais:

- Interface intuitiva para inserção de dados de projetos
- Cálculo automático de KPIs financeiros
- Análise comparativa entre projetos
- Geração de insights e recomendações por IA
- Visualização de dados em tabelas e gráficos

##  Tecnologias Utilizadas

[ Voltar ao índice](#-índice)

**Core:**

- Python 3.12+
- Streamlit 1.39.0+
- Azure OpenAI
- CrewAI


##  Requisitos

[ Voltar ao índice](#-índice)

- Python 3.12 ou superior
- Poetry para gerenciamento de dependências
- Conta Azure com acesso à API Azure OpenAI
- Variáveis de ambiente configuradas corretamente

## ⚙️ Instalação e Execução

###  Execução Local com Poetry

[ Voltar ao índice](#-índice)

1. Clone o repositório:

```bash
git clone https://github.com/Jcnok/MicrosoftInnovationChallange25--ROI-Calculator.git
```

2. Navegue até a pasta do repositório:

```bash
cd MicrosoftInnovationChallange25--ROI-Calculator
```

3. Instale o Poetry (caso não tenha):

```bash
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
```

4. Configure o ambiente virtual e instale as dependências:

```bash
poetry install --no-root
```

5. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

6. Edite o arquivo `.env` com suas credenciais:

```env
AZURE_OPENAI_KEY=sua_chave_openai
AZURE_OPENAI_ENDPOINT=seu_endpoint_openai
#Exemplo:
# AZURE_OPENAI_KEY=2008107cd66943f5b1a99ac461234567
# AZURE_OPENAI_ENDPOINT=https://challange-microsofit-east1.openai.azure.com
```

7. Execute a aplicação:

```bash
poetry run streamlit run src/app.py
```

8. Acesse a aplicação no navegador:

```bash
http://localhost:8501
```

##  Conclusão e Aprendizados

[ Voltar ao índice](#-índice)

Este projeto foi uma excelente oportunidade para aplicar conhecimentos em IA e desenvolvimento web, criando uma ferramenta útil para análise de projetos.

###  Próximos Passos:

- Implementar visualizações gráficas dos KPIs
- Adicionar suporte a mais modelos de IA
- Criar um painel de controle com histórico de projetos
- Otimizar o desempenho da aplicação
- Adicionar atributos como Setor e Região para análise detalhada
- Utilizar azure machine learning para treinamento de modelos
- Salvar os dados em um banco de dados para persistência


Este projeto demonstra o potencial da IA para transformar a análise de projetos e auxiliar na tomada de decisões estratégicas.

---

<div align="center">
  <p>Desenvolvido por:
   Julio Okuda
  </p>
  <p>
   Colaboradores:
   Rodrigo Tenório, Luiz Felipe, João Breno </p>
  <p>LindedIn • Github:</p>
  <p><a href="https://www.linkedin.com/in/juliookuda/">Julio Okuda</a></p>
  <p><a href="https://github.com/rodten23">Rodrigo Tenório</a></p>
  <p><a href="https://github.com/luizfbom">Luiz Felipe</a></p>
  <p><a href="https://github.com/joaobreno4">João Breno</a></p>
</div>
```

