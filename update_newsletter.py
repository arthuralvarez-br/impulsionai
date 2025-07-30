import requests
from bs4 import BeautifulSoup
import feedparser
import datetime

# (Aqui teríamos a lógica completa de coleta de notícias, similar ao curadoria_system_premium.py)
# Para simplificar este exemplo, vamos usar notícias fixas, mas a estrutura está pronta.
def coletar_noticias():
    """
    Esta função simula a coleta de notícias de várias fontes.
    No futuro, podemos colocar aqui a lógica real do seu script de curadoria.
    """
    noticias = [
        {
            "titulo": "IA Generativa pode adicionar até R$4.4 trilhões à economia global, diz McKinsey",
            "fonte": "McKinsey & Company | Estratégia Global",
            "resumo": "Novo relatório da McKinsey destaca o potencial transformador da IA generativa, prevendo um impacto econômico massivo em setores como varejo, bancos e saúde. O estudo enfatiza a necessidade de as empresas investirem em talentos e reestruturação de processos para capturar esse valor."
        },
        {
            "titulo": "Google DeepMind apresenta 'AlphaFold 3', capaz de mapear todas as moléculas da vida",
            "fonte": "Google DeepMind | Inovação Tecnológica",
            "resumo": "O AlphaFold 3 representa um salto quântico na biologia computacional. A nova versão da IA pode prever a estrutura e as interações de proteínas, DNA, RNA e outras moléculas, acelerando drasticamente a descoberta de novos medicamentos e tratamentos para doenças."
        },
        {
            "titulo": "Estudo da FGV aponta que 80% das empresas brasileiras pretendem usar IA para cibersegurança",
            "fonte": "FGV | Mercado Brasileiro 🇧🇷",
            "resumo": "Com o aumento dos ataques cibernéticos, empresas no Brasil estão se voltando para a Inteligência Artificial para prever e neutralizar ameaças em tempo real. A pesquisa da Fundação Getulio Vargas indica que o investimento na área deve triplicar até o final de 2026."
        },
        {
            "titulo": "Como líderes podem preparar suas equipes para a era da colaboração Humano-IA",
            "fonte": "Harvard Business Review | Liderança",
            "resumo": "O foco não é mais substituir humanos, mas sim aumentar suas capacidades. O artigo da HBR oferece um framework para gestores redesenharem fluxos de trabalho, focando em habilidades como pensamento crítico, criatividade e inteligência emocional, áreas onde a sinergia com a IA é mais poderosa."
        }
    ]
    return noticias

def gerar_html_newsletter(noticias):
    """Gera o conteúdo HTML completo para o arquivo newsletter.html."""
    
    # Monta a parte de cada notícia
    html_noticias = ""
    for noticia in noticias:
        html_noticias += f"""
        <article class="news-item">
            <h3>{noticia['titulo']}</h3>
            <span class="source">Fonte: {noticia['fonte']}</span>
            <p>{noticia['resumo']}</p>
        </article>
        """

    # Pega a data atual
    data_hoje = datetime.datetime.now().strftime("%d de %B de %Y")

    # Monta o template HTML completo
    html_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Atual - ImpulsionAI</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: rgba(0, 0, 0, 0.2); padding: 30px; border-radius: 15px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); }}
        header {{ text-align: center; margin-bottom: 40px; }}
        header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
        header p {{ font-size: 1.2rem; color: #ddd; }}
        .newsletter-content h2 {{ color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 10px; margin-bottom: 20px; }}
        .news-item {{ margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.2); }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-item h3 {{ font-size: 1.4rem; margin-bottom: 10px; }}
        .news-item .source {{ font-style: italic; color: #ccc; margin-bottom: 10px; display: block; }}
        .news-item p {{ line-height: 1.6; }}
        .btn-voltar {{ display: inline-block; margin-top: 30px; padding: 12px 25px; background-color: #FFD700; color: #333; text-decoration: none; font-weight: bold; border-radius: 8px; transition: transform 0.2s; }}
        .btn-voltar:hover {{ transform: scale(1.05); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 ImpulsionAI</h1>
            <p>Sua newsletter semanal de IA para líderes brasileiros. Atualizada em: {data_hoje}</p>
        </header>
        <section class="newsletter-content">
            <h2>Newsletter da Semana</h2>
            {html_noticias}
            <div style="text-align: center;">
                <a href="home.html" class="btn-voltar">⬅️ Voltar para a Página Inicial</a>
            </div>
        </section>
    </div>
</body>
</html>"""
    
    return html_completo

if __name__ == "__main__":
    print("Coletando notícias...")
    noticias_coletadas = coletar_noticias()
    
    print("Gerando arquivo HTML da newsletter...")
    html_final = gerar_html_newsletter(noticias_coletadas)
    
    with open("newsletter.html", "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print("Arquivo 'newsletter.html' gerado com sucesso!")

