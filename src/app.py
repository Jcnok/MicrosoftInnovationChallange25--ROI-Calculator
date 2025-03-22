# importa as libs
import os
import numpy as np
import pandas as pd
import streamlit as st
from crewai import LLM, Agent, Task
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da OpenAI Azure
llm = LLM(
    model="azure/gpt-4o-mini",
    api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    temperature=0.1,
)


# --- Funções para cálculos de KPIs ---
def calcular_roi(investimento: float, retorno: float) -> float:
    """Calcula o Retorno sobre o Investimento (ROI).

    Args:
        investimento (float): O valor do investimento.
        retorno (float): O valor do retorno.

    Returns:
        float: O valor do ROI em porcentagem.
    """
    if investimento == 0:
        return np.inf
    return ((retorno - investimento) / investimento) * 100


def calcular_vpl(taxa_desconto: float, fluxos_caixa: list) -> float:
    """Calcula o Valor Presente Líquido (VPL).

    Args:
        taxa_desconto (float): A taxa de desconto anual em porcentagem.
        fluxos_caixa (list): Uma lista dos fluxos de caixa do projeto.

    Returns:
        float: O valor do VPL.
    """
    vpl = 0
    for i, fluxo in enumerate(fluxos_caixa):
        vpl += fluxo / (1 + taxa_desconto / 100) ** i
    return vpl


# --- Agente de Cálculo de KPIs ---
class KPICalculatorAgent:
    """Um agente para calcular KPIs financeiros de projetos."""

    def __init__(self, llm: LLM):
        """Inicializa o KPICalculatorAgent.
        Args:
            llm (LLM): O modelo de linguagem grande a ser usado pelo agente.
        """
        self.agent = Agent(
            role="Especialista em Análise Financeira",
            goal="Calcular KPIs financeiros precisos para avaliar projetos.",
            verbose=True,
            llm=llm,
            backstory="Você é um analista financeiro experiente com um histórico comprovado de avaliação de projetos e identificação de oportunidades de investimento.",
        )

    def calculate_kpis(self, data: dict) -> dict:
        """Calcula os KPIs financeiros com base nos dados do projeto.

        Args:
            data (dict): Um dicionário contendo os dados do projeto.

        Returns:
            dict: Um dicionário contendo os KPIs calculados.
        """
        orcamento = data["orcamento"]
        duracao = data["duracao"]
        custo_treinamento = data["custo_treinamento"]
        custo_implementacao = data["custo_implementacao"]
        economia_custos = data["economia_custos"]
        aumento_receita = data["aumento_receita"]
        taxa_desconto = data["taxa_desconto"]

        investimento_total = orcamento + custo_treinamento + custo_implementacao
        retorno_total = (economia_custos * duracao) + (aumento_receita * duracao)

        roi = calcular_roi(investimento_total, retorno_total)
        vpl = calcular_vpl(
            taxa_desconto,
            [-investimento_total] + [(economia_custos + aumento_receita)] * duracao,
        )

        return {
            "ROI": f"{roi:.2f}",
            "VPL": f"{vpl:.2f}",
            "Investimento Total": f"{investimento_total:.2f}",
            "Retorno Total": f"{retorno_total:.2f}",
        }


# --- Agente de Análise de Resultados ---
class ResultAnalyzerAgent:
    """Um agente para analisar os resultados dos KPIs e fornecer insights."""

    def __init__(self, llm: LLM):
        """Inicializa o ResultAnalyzerAgent.

        Args:
            llm (LLM): O modelo de linguagem grande a ser usado pelo agente.
        """
        self.agent = Agent(
            role="Analista de Projetos Sênior",
            goal="Analisar os KPIs e dados de projetos para fornecer insights valiosos e recomendações acionáveis. Forneça análises concisas e bem formatadas, evitando quebras de linha desnecessárias.",
            verbose=True,
            llm=llm,
            backstory="Você é um analista de projetos experiente, com um olhar crítico para detalhes e uma capacidade de transformar dados em estratégias eficazes. Ao final, deve dar ênfase à Gestão de Mudança e apontar riscos devivo ao ramo de atuação escolhido. É uma premissa sempre informar que a análise foi feita através de uma IA e que recomendado que uma equipe humana faça revisão.",
        )

    def create_analysis_task(self, kpis: dict, data: dict) -> Task:
        """Cria uma tarefa para analisar os KPIs e dados do projeto.

        Args:
            kpis (dict): Um dicionário contendo os KPIs calculados.
            data (dict): Um dicionário contendo os dados do projeto.

        Returns:
            Task: A tarefa de análise criada.
        """
        orcamento = data["orcamento"]
        funcionarios = data["funcionarios"]
        duracao = data["duracao"]
        custo_treinamento = data["custo_treinamento"]
        custo_implementacao = data["custo_implementacao"]
        economia_custos = data["economia_custos"]
        aumento_receita = data["aumento_receita"]
        taxa_desconto = data["taxa_desconto"]
        risco_falha = data["risco_falha"]
        gestao_mudanca = data["gestao_mudanca"]
        ramo_atuacao = data["ramo_atuacao"]

        return Task(
            description=f"""Analise os seguintes KPIs do projeto:
            ROI: {kpis['ROI']}
            VPL: {kpis['VPL']}
            Investimento Total: {kpis['Investimento Total']}
            Retorno Total: {kpis['Retorno Total']}

            Considere também os seguintes dados do projeto:
            Orçamento: {orcamento:.2f}
            Número de Funcionários Impactados: {funcionarios}
            Duração do Projeto: {duracao} meses
            Custo de Treinamento: {custo_treinamento:.2f}
            Custo de Implementação: {custo_implementacao:.2f}
            Economia de Custos: {economia_custos:.2f}
            Aumento de Receita: {aumento_receita:.2f}
            Taxa de Desconto: {taxa_desconto}
            Risco de Falha: {risco_falha}
            Gestão de Mudanças: dificuldade {gestao_mudanca}
            Ramo de Atuação: {ramo_atuacao}

            Onde houver o símbolo de R$ substitua por R\$ para formatação correta.
            Forneça insights sobre a saúde financeira do projeto, identifique problemas potenciais, sugira melhorias e forneça recomendações acionáveis.
            Destaque os pontos fortes e fracos do projeto com base nos dados fornecidos.
            Mantenha a formatação concisa e evite quebras de linha desnecessárias.
            """,
            expected_output="Uma análise detalhada do projeto, com insights, problemas potenciais, sugestões de melhoria e recomendações, formatada de forma clara e concisa.",
            agent=self.agent,
        )

    def analyze_project(self, kpis: dict, data: dict) -> str:
        """Executa a tarefa de análise do projeto.

        Args:
            kpis (dict): Um dicionário contendo os KPIs calculados.
            data (dict): Um dicionário contendo os dados do projeto.

        Returns:
            str: A análise do projeto.
        """
        task = self.create_analysis_task(kpis, data)
        return self.agent.execute_task(task)


# --- Agente de Comparação de Projetos ---
class ProjectComparatorAgent:
    """Um agente para comparar projetos com base em KPIs e análises."""

    def __init__(self, llm: LLM):
        """Inicializa o ProjectComparatorAgent.

        Args:
            llm (LLM): O modelo de linguagem grande a ser usado pelo agente.
        """
        self.agent = Agent(
            role="Especialista em Tomada de Decisões Estratégicas",
            goal="Comparar projetos com base em KPIs e análises para recomendar a melhor opção.",
            verbose=True,
            llm=llm,
            backstory="Você é um líder estratégico com uma habilidade excepcional para avaliar opções, pesar prós e contras, e tomar decisões informadas que impulsionam o sucesso.",
        )

    def compare_projects(
        self,
        projeto_a_analise: str,
        projeto_b_analise: str,
        projeto_a_kpis: dict,
        projeto_b_kpis: dict,
    ) -> str:
        """Compara os projetos com base nas análises e KPIs.

        Args:
            projeto_a_analise (str): A análise do Projeto A.
            projeto_b_analise (str): A análise do Projeto B.
            projeto_a_kpis (dict): Os KPIs do Projeto A.
            projeto_b_kpis (dict): Os KPIs do Projeto B.

        Returns:
            str: A comparação dos projetos e a recomendação.
        """
        task = Task(
            description=f"""Compare os seguintes projetos com base em suas análises e KPIs:

            **Projeto A:**
            Análise: {projeto_a_analise}
            ROI: {projeto_a_kpis['ROI']}
            VPL: {projeto_a_kpis['VPL']}

            **Projeto B:**
            Análise: {projeto_b_analise}
            ROI: {projeto_b_kpis['ROI']}
            VPL: {projeto_b_kpis['VPL']}

            Onde houver o símbolo de R$ substitua por R\$ para formatação correta.
            Destaque as vantagens e desvantagens de cada projeto, considerando os KPIs e os fatores qualitativos.
            Recomende o melhor projeto com base na análise comparativa e justifique sua recomendação.
            """,
            expected_output="Uma comparação detalhada dos projetos, destacando vantagens e desvantagens, e uma recomendação clara com justificativa.",
            agent=self.agent,
        )
        return self.agent.execute_task(task)


# --- Frontend Streamlit ---
st.set_page_config(layout="wide")

# Menu lateral
st.sidebar.title("ROI Vision: Análise Inteligente de Projetos")
menu = st.sidebar.radio("Navegação", ["Página Inicial", "Calculadora de ROI", "Sobre"])

if menu == "Página Inicial":
    st.title("Bem-vindo ao ROI Vision! 🚀")
    st.write(
        "Este projeto foi desenvolvido para o Hackathon da Microsoft e tem como objetivo fornecer uma ferramenta inteligente para análise e comparação de projetos."
    )
    st.write(
        "Utilizando inteligência artificial, o ROI Vision calcula KPIs financeiros cruciais, analisa os resultados e compara projetos, auxiliando na tomada de decisões estratégicas."
    )
    st.write(
        "Navegue até a seção 'Calculadora de ROI' para começar a analisar seus projetos!"
    )

elif menu == "Calculadora de ROI":
    st.title("Calculadora de ROI Comparativa com IA 📊")

    # Criando as colunas para os dados dos projetos
    col1, col2 = st.columns(2)

    # Dados do Projeto A na primeira coluna
    with col1:
        st.header("Projeto A 🚀")
        orcamento_a = st.number_input(
            "Orçamento 💰",
            value=100000.0,
            key="orcamento_a",
            help="Orçamento total previsto para o projeto.",
        )
        funcionarios_a = st.number_input(
            "Número de Funcionários Impactados 🧑‍🤝‍🧑",
            value=100,
            key="funcionarios_a",
            help="Número de funcionários diretamente impactados pelo projeto.",
        )
        duracao_a = st.number_input(
            "Duração (meses) ⏳",
            value=12,
            key="duracao_a",
            help="Duração estimada do projeto em meses.",
        )
        custo_treinamento_a = st.number_input(
            "Custo de Treinamento 📚",
            value=5000.0,
            key="custo_treinamento_a",
            help="Custo total com treinamento para o projeto.",
        )
        custo_implementacao_a = st.number_input(
            "Custo de Implementação 🛠️",
            value=10000.0,
            key="custo_implementacao_a",
            help="Custo total com a implementação do projeto.",
        )
        economia_custos_a = st.number_input(
            "Economia de Custos 📉",
            value=8000.0,
            key="economia_custos_a",
            help="Economia de custos mensal esperada após a implementação do projeto.",
        )
        aumento_receita_a = st.number_input(
            "Aumento de Receita 📈",
            value=15000.0,
            key="aumento_receita_a",
            help="Aumento de receita mensal esperado após a implementação do projeto.",
        )
        taxa_desconto_a = st.number_input(
            "Taxa de Desconto (%) ✂️",
            value=10.0,
            key="taxa_desconto_a",
            help="Taxa de desconto anual a ser utilizada no cálculo do VPL.",
        )
        risco_falha_a = st.number_input(
            "Risco de Falha (%) ⚠️",
            value=5.0,
            key="risco_falha_a",
            help="Probabilidade estimada de falha do projeto.",
        )
        dificuldade_gestao_mudanca_a = st.selectbox(
            "Dificuldade para Gestão de Mudança ⚠️", ["Fácil", "Médio", "Difícil"],
            key="dificuldade_gestao_mudanca_a",
            help="Provável nível de dificuldade para a gestão de mudança.",
        )
        ramo_atuacao_a = st.selectbox(
            "Ramo de atuação ⚠️", ["Serviços - Alimentação", "Serviços - Educação", "Serviços - Saúde", "Indústria - Gráfica", "Indústria - Automotiva", "Indústria - Têxtil", "Agronomia", "Geração de Energia", "TI - IA"],
            key="ramo_atuacao_a",
            help="Ramo de atuação do projeto.",
        )

    # Dados do Projeto B na segunda coluna
    with col2:
        st.header("Projeto B 🎯")
        orcamento_b = st.number_input(
            "Orçamento 💰",
            value=150000.0,
            key="orcamento_b",
            help="Orçamento total previsto para o projeto.",
        )
        funcionarios_b = st.number_input(
            "Número de Funcionários Impactados 🧑‍🤝‍🧑",
            value=150,
            key="funcionarios_b",
            help="Número de funcionários diretamente impactados pelo projeto.",
        )
        duracao_b = st.number_input(
            "Duração (meses) ⏳",
            value=18,
            key="duracao_b",
            help="Duração estimada do projeto em meses.",
        )
        custo_treinamento_b = st.number_input(
            "Custo de Treinamento 📚",
            value=7000.0,
            key="custo_treinamento_b",
            help="Custo total com treinamento para o projeto.",
        )
        custo_implementacao_b = st.number_input(
            "Custo de Implementação 🛠️",
            value=12000.0,
            key="custo_implementacao_b",
            help="Custo total com a implementação do projeto.",
        )
        economia_custos_b = st.number_input(
            "Economia de Custos 📉",
            value=10000.0,
            key="economia_custos_b",
            help="Economia de custos mensal esperada após a implementação do projeto.",
        )
        aumento_receita_b = st.number_input(
            "Aumento de Receita 📈",
            value=20000.0,
            key="aumento_receita_b",
            help="Aumento de receita mensal esperado após a implementação do projeto.",
        )
        taxa_desconto_b = st.number_input(
            "Taxa de Desconto (%) ✂️",
            value=12.0,
            key="taxa_desconto_b",
            help="Taxa de desconto anual a ser utilizada no cálculo do VPL.",
        )
        risco_falha_b = st.number_input(
            "Risco de Falha (%) ⚠️",
            value=8.0,
            key="risco_falha_b",
            help="Probabilidade estimada de falha do projeto.",
        )
        dificuldade_gestao_mudanca_b = st.selectbox(
            "Dificuldade para Gestão de Mudança ⚠️", ["Fácil", "Médio", "Difícil"],
            key="dificuldade_gestao_mudanca_b",
            help="Provável nível de dificuldade para a gestão de mudança.",
        )
        ramo_atuacao_b = st.selectbox(
            "Ramo de atuação ⚠️", ["Serviços - Alimentação", "Serviços - Educação", "Serviços - Saúde", "Indústria - Gráfica", "Indústria - Automotiva", "Indústria - Têxtil", "Agronomia", "Geração de Energia", "TI - IA"],
            key="ramo_atuacao_b",
            help="Ramo de atuação do projeto.",
        )

    dados_projeto_a = {
        "orcamento": orcamento_a,
        "funcionarios": funcionarios_a,
        "duracao": duracao_a,
        "custo_treinamento": custo_treinamento_a,
        "custo_implementacao": custo_implementacao_a,
        "economia_custos": economia_custos_a,
        "aumento_receita": aumento_receita_a,
        "taxa_desconto": taxa_desconto_a,
        "risco_falha": risco_falha_a,
        "gestao_mudanca": dificuldade_gestao_mudanca_a,
        "ramo_atuacao": ramo_atuacao_a,
    }

    dados_projeto_b = {
        "orcamento": orcamento_b,
        "funcionarios": funcionarios_b,
        "duracao": duracao_b,
        "custo_treinamento": custo_treinamento_b,
        "custo_implementacao": custo_implementacao_b,
        "economia_custos": economia_custos_b,
        "aumento_receita": aumento_receita_b,
        "taxa_desconto": taxa_desconto_b,
        "risco_falha": risco_falha_b,
        "gestao_mudanca": dificuldade_gestao_mudanca_b,
        "ramo_atuacao": ramo_atuacao_b,
    }

    if st.button("Analisar Projetos ✅"):
        kpi_calculator = KPICalculatorAgent(llm)
        result_analyzer = ResultAnalyzerAgent(llm)
        project_comparator = ProjectComparatorAgent(llm)

        # Calcular KPIs
        kpis_projeto_a = kpi_calculator.calculate_kpis(dados_projeto_a)
        kpis_projeto_b = kpi_calculator.calculate_kpis(dados_projeto_b)

        # Analisar projetos
        analise_resultado_a = result_analyzer.analyze_project(
            kpis_projeto_a, dados_projeto_a
        )
        analise_resultado_b = result_analyzer.analyze_project(
            kpis_projeto_b, dados_projeto_b
        )

        # Comparar projetos
        comparacao_projetos = project_comparator.compare_projects(
            analise_resultado_a, analise_resultado_b, kpis_projeto_a, kpis_projeto_b
        )

        # Salvar dados em DataFrame
        data = {
            "Projeto": ["A", "B"],
            "Orçamento R$": [
                f"{dados_projeto_a['orcamento']:.2f}",
                f"{dados_projeto_b['orcamento']:.2f}",
            ],
            "Funcionários Impactados": [
                dados_projeto_a["funcionarios"],
                dados_projeto_b["funcionarios"],
            ],
            "Duração (meses)": [dados_projeto_a["duracao"], dados_projeto_b["duracao"]],
            "Custo de Treinamento R$": [
                f"{dados_projeto_a['custo_treinamento']:.2f}",
                f"{dados_projeto_b['custo_treinamento']:.2f}",
            ],
            "Custo de Implementação R$": [
                f"{dados_projeto_a['custo_implementacao']:.2f}",
                f"{dados_projeto_b['custo_implementacao']:.2f}",
            ],
            "Economia de Custos R$": [
                f"{dados_projeto_a['economia_custos']:.2f}",
                f"{dados_projeto_b['economia_custos']:.2f}",
            ],
            "Aumento de Receita R$": [
                f"{dados_projeto_a['aumento_receita']:.2f}",
                f"{dados_projeto_b['aumento_receita']:.2f}",
            ],
            "Taxa de Desconto (%)": [
                f"{dados_projeto_a['taxa_desconto']:.2f}%",
                f"{dados_projeto_b['taxa_desconto']:.2f}%",
            ],
            "Risco de Falha (%)": [
                f"{dados_projeto_a['risco_falha']:.2f}%",
                f"{dados_projeto_b['risco_falha']:.2f}%",
            ],
            "Gestão de Mudança": [
                dados_projeto_a['gestao_mudanca'],
                dados_projeto_b['gestao_mudanca'],
            ],
            "Ramo": [
                dados_projeto_a['ramo_atuacao'],
                dados_projeto_b['ramo_atuacao'],
            ],
            "ROI (%)": [kpis_projeto_a["ROI"], kpis_projeto_b["ROI"]],
            "VPL R$": [kpis_projeto_a["VPL"], kpis_projeto_b["VPL"]],
            "Investimento Total R$": [
                kpis_projeto_a["Investimento Total"],
                kpis_projeto_b["Investimento Total"],
            ],
            "Retorno Total R$": [
                kpis_projeto_a["Retorno Total"],
                kpis_projeto_b["Retorno Total"],
            ],
        }
        df = pd.DataFrame(data)

        # Exibir DataFrame
        st.subheader("Dados dos Projetos e KPIs 📊")
        st.dataframe(df)

        # Exibir resultados
        st.header("Resultados da Análise 🔍")

        # Exibir KPIs em tabelas
        st.subheader("KPIs dos Projetos 📈")
        col_kpi_a, col_kpi_b = st.columns(2)

        with col_kpi_a:
            st.write("Projeto A")
            kpi_df_a = pd.DataFrame([kpis_projeto_a])
            st.table(kpi_df_a)
            st.latex(
                r"""
                ROI=\frac{Retorno - Investimento}{Investimento} \times 100
            """
            )

        with col_kpi_b:
            st.write("Projeto B")
            kpi_df_b = pd.DataFrame([kpis_projeto_b])
            st.table(kpi_df_b)
            st.latex(
                r"""
                VPL=\sum_{t=0}^{n} \frac{Fluxo\ de\ Caixa_t}{(1 + Taxa\ de\ Desconto)^t}
            """
            )

        st.subheader("Análises dos Projetos 🧐")
        col_analise_a, col_analise_b = st.columns(2)

        with col_analise_a:
            st.write("Projeto A")
            st.markdown(analise_resultado_a)

        with col_analise_b:
            st.write("Projeto B")
            st.markdown(analise_resultado_b)

        # Exibir comparação com Markdown
        st.subheader("Comparação dos Projetos ⚖️")
        st.markdown(comparacao_projetos)

elif menu == "Sobre":
    st.title("Sobre o ROI Vision 💡")
    st.subheader("Limitações:")
    st.write("- Toda análise apresentada por este sistema é feita por IAm sendo recomendado que uma equipe humana faça revisão, afim de garantir a precisão das análises.")
    st.write("- Informamos que nenhum dado do usuário é armazenado e que apenas o nosso parceiro de IA tem acesso aos dados informados, seguindo as Leis e recomendações para tratamento de dados.")
    st.subheader('Equipe "BlueSky Team":')
    st.write("Idealização e Desenvolvimento: JULIO OKUDA - [LinkedIn](https://www.linkedin.com/in/juliookuda/) - [GitHub](https://github.com/Jcnok)")
    st.write("Apoio e Revisão: RODRIGO ALVES TENÓRIO - [LinkedIn](https://www.linkedin.com/in/rodrigoalvestenorio) - [GitHub](https://github.com/rodten23)")
    st.write("LUIZ FELIPE - [LinkedIn](https://www.linkedin.com/in/) - [GitHub](https://github.com/)")
    st.write("JOÃO BRENO - [LinkedIn](https://www.linkedin.com/in/) - [GitHub](https://github.com/)")
    st.subheader("Tecnologias utilizadas:")
    st.write("- Streamlit")
    st.write("- Azure OpenAI")
    st.write("- CrewAI")
    st.write("- Python")
    st.write("- Pandas")
    st.write("- Numpy")
    st.write("- Dotenv")
    st.write("© 2025 Todos os direitos reservados")
