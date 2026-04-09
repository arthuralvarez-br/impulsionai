"""
update_newsletter.py
ImpulsionAI — Coleta via RSS + curadoria com Claude API

Publico: lideres de 35 a 65 anos, gestores, profissionais liberais, autonomos.
NAO sao de TI. Precisam entender o impacto da IA em gestao, decisao e pessoas.

Uso:
    ANTHROPIC_API_KEY=sk-... python update_newsletter.py

Dependencias:
    pip install feedparser requests anthropic
"""

import feedparser
import datetime
import os
import json
import anthropic

FONTES = [
    {"nome": "Harvard Business Review", "url": "https://hbr.org/topic/artificial-intelligence.rss", "categoria": "Lideranca", "idioma": "en", "grupo": "A"},
    {"nome": "MIT Sloan Management Review", "url": "https://sloanreview.mit.edu/topic/artificial-intelligence/feed/", "categoria": "Gestao", "idioma": "en", "grupo": "A"},
    {"nome": "McKinsey Insights", "url": "https://www.mckinsey.com/rss/insight.rss", "categoria": "Estrategia", "idioma": "en", "grupo": "A"},
    {"nome": "Deloitte Insights", "url": "https://www2.deloitte.com/us/en/insights/rss.xml", "categoria": "Negocios", "idioma": "en", "grupo": "A"},
    {"nome": "World Economic Forum", "url": "https://www.weforum.org/agenda/artificial-intelligence/rss", "categoria": "Global", "idioma": "en", "grupo": "A"},
    {"nome": "OpenAI", "url": "https://openai.com/news/rss.xml", "categoria": "OpenAI", "idioma": "en", "grupo": "B"},
    {"nome": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml", "categoria": "Google", "idioma": "en", "grupo": "B"},
    {"nome": "Microsoft AI", "url": "https://blogs.microsoft.com/ai/feed/", "categoria": "Microsoft", "idioma": "en", "grupo": "B"},
    {"nome": "Meta AI", "url": "https://ai.meta.com/blog/rss/", "categoria": "Meta", "idioma": "en", "grupo": "B"},
    {"nome": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "categoria": "Lancamentos", "idioma": "en", "grupo": "B"},
    {"nome": "MIT Technology Review", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed", "categoria": "Pesquisa", "idioma": "en", "grupo": "B"},
    {"nome": "Exame Tecnologia", "url": "https://exame.com/tecnologia/feed/", "categoria": "Brasil", "idioma": "pt", "grupo": "C"},
    {"nome": "Canaltech IA", "url": "https://canaltech.com.br/rss/inteligencia-artificial/", "categoria": "Brasil", "idioma": "pt", "grupo": "C"},
]

MAX_POR_FONTE = 3
MAX_TOTAL = 8


def coletar_rss():
    artigos = []
    for fonte in FONTES:
        try:
            feed = feedparser.parse(fonte["url"])
            coletados = 0
            for entry in feed.entries:
                if coletados >= MAX_POR_FONTE:
                    break
                titulo = entry.get("title", "").strip()
                resumo = entry.get("summary", entry.get("description", "")).strip()
                link = entry.get("link", "").strip()
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    data = datetime.datetime(*entry.published_parsed[:6])
                else:
                    data = datetime.datetime.now()
                if titulo and link:
                    artigos.append({
                        "titulo": titulo,
                        "resumo": resumo[:500] if resumo else "",
                        "link": link,
                        "fonte": fonte["nome"],
                        "categoria": fonte["categoria"],
                        "grupo": fonte["grupo"],
                        "data": data.strftime("%d de %B de %Y"),
                    })
                    coletados += 1
        except Exception as e:
            print(f"  [AVISO] Falha ao coletar {fonte['nome']}: {e}")
    print(f"  Coletados {len(artigos)} artigos brutos.")
    return artigos


def curar_com_ia(artigos):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("Defina ANTHROPIC_API_KEY antes de rodar.")

    client = anthropic.Anthropic(api_key=api_key)

    lista_raw = "\n".join(
        f"[{i+1}] GRUPO:{a['grupo']} | TITULO: {a['titulo']}\n"
        f"    FONTE: {a['fonte']} | CATEGORIA: {a['categoria']} | DATA: {a['data']}\n"
        f"    RESUMO: {a['resumo'][:300]}\n"
        f"    LINK: {a['link']}"
        for i, a in enumerate(artigos)
    )

    prompt = (
        "Voce e o editor da newsletter ImpulsionAI.\n\n"
        "PERFIL DO LEITOR:\n"
        "- Lider brasileiro entre 35 e 65 anos, pos-graduado.\n"
        "- Nao e profissional de TI. E gestor, autonomo, profissional liberal.\n"
        "- Pergunta central: O que isso muda para mim, minha equipe e minha organizacao?\n\n"
        "CRITERIOS DE SELECAO:\n"
        "1. Impacto em gestao de pessoas, tomada de decisao, planejamento\n"
        "2. Ferramenta de IA que um lider nao-tecnico pode usar hoje\n"
        "3. Mudanca de cenario que afeta posicionamento organizacional\n"
        "4. Contexto brasileiro\n\n"
        "DESCARTAR: arquitetura de modelos, benchmarks, valuations, conteudo tecnico.\n"
        "Maximo 2 artigos por empresa.\n\n"
        "RESUMO: 2 frases. Primeira: o que aconteceu. Segunda: o que muda para um lider.\n"
        "IMPACTO: Alto, Medio ou Observar.\n"
        "NUNCA invente dados. Responda APENAS JSON valido.\n\n"
        f"Selecione exatamente {MAX_TOTAL} artigos.\n\n"
        "Formato:\n"
        "[\n  {\n"
        '    "titulo": "...",\n'
        '    "fonte": "...",\n'
        '    "categoria": "...",\n'
        '    "data": "...",\n'
        '    "resumo": "...",\n'
        '    "link": "...",\n'
        '    "impacto": "Alto | Medio | Observar"\n'
        "  }\n]\n\n"
        f"Artigos disponiveis:\n{lista_raw}"
    )

    print("  Enviando para curadoria via Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    texto = message.content[0].text.strip()
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
        texto = texto.strip()

    curados = json.loads(texto)
    print(f"  IA selecionou {len(curados)} artigos.")
    return curados[:MAX_TOTAL]


IMPACTO_CONFIG = {
    "Alto": {"cor": "#c9a84c", "bg": "rgba(201,168,76,0.10)"},
    "Medio": {"cor": "rgba(255,255,255,0.45)", "bg": "rgba(255,255,255,0.04)"},
    "Observar": {"cor": "rgba(255,255,255,0.22)", "bg": "rgba(255,255,255,0.02)"},
}


def normalizar_impacto(raw):
    r = raw.lower()
    if "alto" in r:
        return "Alto"
    if "medio" in r or "medio" in r:
        return "Medio"
    return "Observar"


def gerar_html(noticias):
    data_hoje = datetime.datetime.now().strftime("%d de %B de %Y")

    cards = ""
    for n in noticias:
        impacto = normalizar_impacto(n.get("impacto", "Observar"))
        cfg = IMPACTO_CONFIG[impacto]
        label = "Medio" if impacto == "Medio" else impacto
        cards += (
            f'\n<article class="news-item" style="border-left:3px solid {cfg["cor"]};background:{cfg["bg"]};">\n'
            f'<div class="news-meta">\n'
            f'<span class="news-tag">{n.get("categoria","")}</span>\n'
            f'<span class="news-impact" style="color:{cfg["cor"]};">- {label}</span>\n'
            f'<span class="news-date">{n.get("data","")}</span>\n'
            f'</div>\n'
            f'<h3 class="news-title">{n["titulo"]}</h3>\n'
            f'<p class="news-body">{n.get("resumo","")}</p>\n'
            f'<div class="news-footer">\n'
            f'<span class="news-source">{n.get("fonte","")}</span>\n'
            f'<a href="{n.get("link","#")}" target="_blank" rel="noopener" class="read-btn">Leia a materia completa</a>\n'
            f'</div>\n'
            f'</article>'
        )

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ImpulsionAI - """ + data_hoje + """</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{--ink:#0a0a0f;--paper:#f5f0e8;--gold:#c9a84c;--muted:#6b6b6b;--white:#ffffff;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'DM Sans',sans-serif;background:var(--paper);color:var(--ink);}
header{background:var(--ink);padding:48px 60px;}
.header-inner{max-width:860px;margin:0 auto;}
.logo{font-family:'Playfair Display',serif;font-size:1.4rem;color:var(--white);margin-bottom:20px;}
.logo span{color:var(--gold);}
header h1{font-family:'Playfair Display',serif;font-size:2.3rem;font-weight:900;color:var(--white);line-height:1.15;}
header h1 em{font-style:italic;color:var(--gold);}
.edition-info{margin-top:10px;font-size:0.73rem;letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.2);}
main{max-width:860px;margin:0 auto;padding:54px 60px 96px;}
.section-label{font-size:0.71rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--gold);font-weight:500;margin-bottom:34px;padding-bottom:14px;border-bottom:1px solid rgba(0,0,0,0.1);}
.news-item{padding:26px 22px;margin-bottom:10px;border-radius:3px;}
.news-meta{display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap;}
.news-tag{font-size:0.66rem;letter-spacing:0.15em;text-transform:uppercase;font-weight:500;background:rgba(0,0,0,0.07);color:var(--muted);padding:3px 9px;border-radius:2px;}
.news-impact{font-size:0.69rem;letter-spacing:0.08em;font-weight:700;text-transform:uppercase;}
.news-date{font-size:0.71rem;color:rgba(0,0,0,0.26);margin-left:auto;}
.news-title{font-family:'Playfair Display',serif;font-size:1.22rem;font-weight:700;color:var(--ink);line-height:1.32;margin-bottom:10px;}
.news-body{font-size:0.88rem;color:var(--muted);line-height:1.72;margin-bottom:16px;}
.news-footer{display:flex;justify-content:space-between;align-items:center;}
.news-source{font-size:0.69rem;letter-spacing:0.08em;text-transform:uppercase;color:rgba(0,0,0,0.24);}
.read-btn{font-size:0.8rem;font-weight:500;color:var(--gold);text-decoration:none;}
.wa-block{margin-top:54px;background:var(--ink);padding:30px 34px;border-radius:4px;display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;}
.wa-text h3{font-family:'Playfair Display',serif;font-size:1.1rem;color:var(--white);margin-bottom:4px;}
.wa-text p{font-size:0.8rem;color:rgba(255,255,255,0.36);}
.wa-btn{display:inline-flex;align-items:center;gap:8px;background:var(--gold);color:var(--ink);padding:12px 24px;border-radius:3px;font-size:0.82rem;font-weight:700;text-decoration:none;}
.editorial{margin-top:48px;padding:36px 40px;background:rgba(0,0,0,0.03);border:1px solid rgba(0,0,0,0.07);border-radius:4px;}
.editorial-tag{font-size:0.68rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--gold);font-weight:600;}
.editorial-header{margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid rgba(0,0,0,0.07);}
.editorial-text{font-size:0.88rem;color:var(--muted);line-height:1.72;}
.eco-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:24px 0;}
.eco-item{display:flex;align-items:flex-start;gap:12px;padding:14px 16px;background:var(--white);border-radius:3px;border:1px solid rgba(0,0,0,0.06);}
.eco-icon{font-size:1.1rem;flex-shrink:0;margin-top:2px;}
.eco-content{display:flex;flex-direction:column;gap:3px;}
.eco-content strong{font-size:0.86rem;color:var(--ink);font-weight:600;}
.eco-content span{font-size:0.80rem;color:var(--muted);line-height:1.5;}
.eco-contact{font-size:0.8rem;color:rgba(0,0,0,0.38);margin-top:6px;}
.eco-contact a{color:var(--gold);text-decoration:none;}
.back-link{display:inline-block;margin-top:34px;font-size:0.8rem;color:var(--muted);text-decoration:none;}
footer{background:var(--ink);padding:26px 60px;text-align:center;font-size:0.71rem;color:rgba(255,255,255,0.15);}
@media(max-width:768px){header,main,footer{padding-left:20px;padding-right:20px;}.eco-grid{grid-template-columns:1fr;}.wa-block{flex-direction:column;}}
</style>
</head>
<body>
<header>
<div class="header-inner">
<div class="logo">Impulsion<span>AI</span></div>
<h1>IA para quem lidera.<br><em>Edicao de """ + data_hoje + """</em></h1>
<p class="edition-info">Pilar: Uso de Tecnologias Emergentes - Triade da Nova Lideranca - Semanal</p>
</div>
</header>
<main>
<p class="section-label">O que esta mudando esta semana</p>
""" + cards + """
<div class="wa-block">
<div class="wa-text">
<h3>Grupo ImpulsionAI no WhatsApp</h3>
<p>210+ lideres. Discussoes praticas sobre IA em gestao e decisao.</p>
</div>
<a href="https://chat.whatsapp.com/GcnYSlUkcE0K3utFJgx9nz" target="_blank" class="wa-btn">Entrar no grupo</a>
</div>
<div class="editorial">
<div class="editorial-header"><span class="editorial-tag">Da redacao</span></div>
<p class="editorial-text">O que voce leu esta semana e parte do pilar <strong>Uso de Tecnologias Emergentes</strong> da Triade da Nova Lideranca. Entender o cenario e o primeiro passo. O segundo e saber como aplicar isso a sua realidade, a sua equipe e as suas decisoes.</p>
<p class="editorial-text" style="margin-top:10px;">Se voce sente que precisa ir alem da leitura, o ecossistema ImpulsionAI oferece caminhos concretos.</p>
<div class="eco-grid">
<div class="eco-item"><span class="eco-icon">🎯</span><div class="eco-content"><strong>Mentoria individual e em grupo</strong><span>Uso de IA aplicado a sua gestao, negocios e planejamento.</span></div></div>
<div class="eco-item"><span class="eco-icon">📊</span><div class="eco-content"><strong>Dashboards de gestao com IA</strong><span>Paineis para decisao, RH e acompanhamento estrategico.</span></div></div>
<div class="eco-item"><span class="eco-icon">🧠</span><div class="eco-content"><strong>GRAFOBOT</strong><span>Parecer Neurocognitivo da Escrita para mensuracao de perfil comportamental.</span></div></div>
<div class="eco-item"><span class="eco-icon">💚</span><div class="eco-content"><strong>Pulsovital</strong><span>Termometro de estresse e autocuidado para lideres e equipes.</span></div></div>
<div class="eco-item"><span class="eco-icon">🏆</span><div class="eco-content"><strong>Treinamentos e PDIs</strong><span>Programas de desenvolvimento personalizados para times.</span></div></div>
<div class="eco-item"><span class="eco-icon">🤖</span><div class="eco-content"><strong>IAprender</strong><span>Alfabetizacao pratica em IA para profissionais que querem usar.</span></div></div>
</div>
<p class="eco-contact">Quer conversar? <a href="https://www.grafobot.com.br">grafobot.com.br</a> - <a href="https://www.pulsovital.com.br">pulsovital.com.br</a></p>
</div>
<a href="index.html" class="back-link">Voltar para a pagina inicial</a>
</main>
<footer>ImpulsionAI - Tabula Rasa Consultoria - Atibaia, SP - """ + data_hoje + """</footer>
</body>
</html>"""
    return html


def main():
    print("-- ImpulsionAI: atualizando newsletter --")
    artigos = coletar_rss()
    curados = curar_com_ia(artigos)
    html = gerar_html(curados)
    with open("newsletter.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("  newsletter.html gerado com sucesso.")
    print("-- Concluido. --")


if __name__ == "__main__":
    main()
