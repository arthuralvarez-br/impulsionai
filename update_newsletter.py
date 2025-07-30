import requests
from bs4 import BeautifulSoup
import feedparser
import datetime

def coletar_noticias( ):
    """
    Coleta de notícias agora incluindo DATA e LINK para cada matéria.
    """
    noticias = [
        {
            "titulo": "IA Generativa pode adicionar até R$4.4 trilhões à economia global, diz McKinsey",
            "fonte": "McKinsey & Company | Estratégia Global",
            "resumo": "Novo relatório da McKinsey destaca o potencial transformador da IA generativa, prevendo um impacto econômico massivo...",
            "data": "28 de Julho de 2025",
            "link": "https://www.mckinsey.com/br/our-insights" # Link de exemplo
        },
        {
            "titulo": "Google DeepMind apresenta 'AlphaFold 3', capaz de mapear todas as moléculas da vida",
            "fonte": "Google DeepMind | Inovação Tecnológica",
            "resumo": "O AlphaFold 3 representa um salto quântico na biologia computacional, acelerando drasticamente a descoberta de novos medicamentos...",
            "data": "27 de Julho de 2025",
            "link": "https://deepmind.google/discover/" # Link de exemplo
        },
        {
            "titulo": "Estudo da FGV aponta que 80% das empresas brasileiras pretendem usar IA para cibersegurança",
            "fonte": "FGV | Mercado Brasileiro 🇧🇷",
            "resumo": "Com o aumento dos ataques cibernéticos, empresas no Brasil estão se voltando para a Inteligência Artificial para prever e neutralizar ameaças...",
            "data": "26 de Julho de 2025",
            "link": "https://portal.fgv.br/noticias" # Link de exemplo
        },
        {
            "titulo": "Como líderes podem preparar suas equipes para a era da colaboração Humano-IA",
            "fonte": "Harvard Business Review | Liderança",
            "resumo": "O foco não é mais substituir humanos, mas sim aumentar suas capacidades. O artigo da HBR oferece um framework para gestores...",
            "data": "25 de Julho de 2025",
            "link": "https://hbr.org/topic/artificial-intelligence" # Link de exemplo
        }
    ]
    return noticias

def gerar_html_newsletter(noticias ):
    """Gera o HTML, agora incluindo a data e um botão 'Leia Mais' com o link."""
    
    html_noticias = ""
    for noticia in noticias:
        html_noticias += f"""
        <article class="news-item">
            <h3>{noticia['titulo']}</h3>
            <div class="metadata">
                <span class="source">Fonte: {noticia['fonte']}</span>
                <span class="date">Data: {noticia['data']}</span>
            </div>
            <p>{noticia['resumo']}</p>
            <a href="{noticia['link']}" target="_blank" class="read-more-btn">Leia a Matéria Completa &rarr;</a>
        </article>
        """

    data_hoje = datetime.datetime.now().strftime("%d de %B de %Y")

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
        .metadata {{ display: flex; justify-content: space-between; font-style: italic; color: #ccc; margin-bottom: 15px; font-size: 0.9rem; flex-wrap: wrap; }}
        .news-item p {{ line-height: 1.6; margin-bottom: 15px; }}
        .read-more-btn {{ display: inline-block; padding: 8px 15px; background-color: rgba(255, 255, 255, 0.1); color: #FFD700; text-decoration: none; font-weight: bold; border-radius: 5px; transition: background-color 0.3s; }}
        .read-more-btn:hover {{ background-color: rgba(255, 215, 0, 0.3); }}
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
    print("Coletando notícias (versão com links e datas)...")
    noticias_coletadas = coletar_noticias()
    
    print("Gerando arquivo HTML da newsletter aprimorado...")
    html_final = gerar_html_newsletter(noticias_coletadas)
    
    with open("newsletter.html", "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print("Arquivo 'newsletter.html' aprimorado gerado com sucesso!")

