#!/usr/bin/env python3
"""Gera as páginas estáticas do site da LG Business.

Uso: python3 _build/build.py   (a partir da raiz do repositório)
Edite os textos aqui e rode de novo; o HTML gerado vai para a raiz.
"""
import csv
import json
import os
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHATS = "5514991030944"
FONE = "(14) 99103-0944"
EMAIL = "atendimento@lgbusiness.adm.br"
ENDERECO = "Rua Gérson França, 6-34, Centro, Bauru/SP, CEP 17015-200"
HORARIO = "Segunda a sexta, das 9h às 17h"
MAPA = "https://www.google.com/maps/search/?api=1&query=" + quote("LG Business, Rua Gérson França 6-34, Centro, Bauru SP")
DOMINIO = "https://lgbusiness.adm.br"


def wa(texto):
    return f"https://wa.me/{WHATS}?text={quote(texto)}"


MENU = [
    ("endereco-fiscal-bauru", "Endereço fiscal"),
    ("salas-e-coworking", "Salas"),
    ("bpo-financeiro", "BPO financeiro"),
    ("imoveis", "Imóveis"),
    ("compra-e-venda-de-empresas", "Compra e venda de empresas"),
    ("contato", "Contato"),
]

MARCA_SVG = (
    '<svg width="34" height="22" viewBox="0 0 34 22" aria-hidden="true">'
    '<rect x="1" y="1" width="32" height="20" rx="2" fill="#b08a3e"/>'
    '<rect x="1" y="1" width="32" height="20" rx="2" fill="none" stroke="#082831" stroke-width="1.5"/>'
    '<circle cx="5.5" cy="11" r="1.4" fill="#082831"/><circle cx="28.5" cy="11" r="1.4" fill="#082831"/>'
    '<text x="17" y="15" text-anchor="middle" font-family="Archivo, sans-serif" font-weight="800" font-size="10" fill="#082831">LG</text>'
    "</svg>"
)


def pagina(caminho, titulo, descricao, corpo, pagina_id, extra_head="", raiz=""):
    caminho = caminho.rstrip("/")
    itens = []
    for href, rotulo in MENU:
        atual = ' aria-current="page"' if caminho == href else ""
        itens.append(f'<a href="{raiz}{href}"{atual}>{rotulo}</a>')
    menu_html = "\n        ".join(itens)
    canonico = DOMINIO + "/" + caminho
    msg_padrao = "Olá! Vim pelo site da LG Business e gostaria de mais informações."
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{extra_head}<title>{titulo}</title>
<meta name="description" content="{descricao}">
<link rel="canonical" href="{canonico}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<link rel="icon" href="{raiz}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{raiz}site.css">
</head>
<body data-raiz="{raiz}" data-pagina="{pagina_id}">
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="conteiner">
    <a class="marca" href="{raiz or './'}">{MARCA_SVG}<span>LG Business</span></a>
    <button class="botao-menu" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav id="menu" class="menu" aria-label="Principal">
        {menu_html}
        <a class="botao whats" href="{wa(msg_padrao)}" target="_blank" rel="noopener" data-origem="menu">WhatsApp</a>
    </nav>
  </div>
</header>
<main id="conteudo">
{corpo}
</main>
<footer class="rodape">
  <div class="conteiner">
    <div class="colunas">
      <div>
        <h2>LG Business</h2>
        <p>Centro de negócios no Centro de Bauru: endereço fiscal, salas, BPO financeiro, imóveis e compra e venda de empresas.</p>
        <p><a href="{MAPA}" target="_blank" rel="noopener">{ENDERECO}</a></p>
      </div>
      <div>
        <h2>Atendimento</h2>
        <ul>
          <li><a href="{wa(msg_padrao)}" target="_blank" rel="noopener" data-origem="rodape">WhatsApp {FONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{HORARIO}</li>
        </ul>
      </div>
      <div>
        <h2>Páginas</h2>
        <ul>
          {"".join(f'<li><a href="{raiz}{h}">{r}</a></li>' for h, r in MENU)}
          <li><a href="{raiz}politica-de-privacidade">Política de privacidade</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>L.G. Business Ltda., CNPJ 08.468.684/0001-62.<br>Corretor responsável: Nelson de Castro Ramos Neto, CRECI 101.538-F.</p>
    </div>
  </div>
</footer>
<a class="whats-flutuante" href="{wa(msg_padrao)}" target="_blank" rel="noopener" data-origem="flutuante">WhatsApp</a>
<script src="{raiz}site.js"></script>
</body>
</html>
"""
    destino = os.path.join(RAIZ, (caminho or "index") + ".html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)


def planos_html(origem):
    return f"""
    <div class="planos">
      <div class="plano">
        <h3>Endereço fiscal</h3>
        <p class="para">Para prestadores de serviço e MEI</p>
        <div class="preco">R$ 149<small>/mês</small></div>
        <ul>
          <li>Endereço no Centro para o CNPJ</li>
          <li>Mesa identificada com o nome da empresa</li>
          <li>Recebimento de correspondências com aviso pelo WhatsApp</li>
        </ul>
        <a class="botao claro" href="{wa('Olá! Quero contratar o plano Endereço fiscal (R$ 149/mês).')}" target="_blank" rel="noopener" data-origem="{origem}-servicos">Contratar este plano</a>
      </div>
      <div class="plano destaque">
        <h3>Endereço fiscal comércio</h3>
        <p class="para">Para empresas com Inscrição Estadual</p>
        <div class="preco">R$ 199<small>/mês</small></div>
        <ul>
          <li>Tudo do plano Endereço fiscal</li>
          <li>Endereço aceito para empresas de comércio</li>
          <li>Apoio na documentação do imóvel para o registro</li>
        </ul>
        <a class="botao claro" href="{wa('Olá! Quero contratar o plano Endereço fiscal comércio (R$ 199/mês).')}" target="_blank" rel="noopener" data-origem="{origem}-comercio">Contratar este plano</a>
      </div>
      <div class="plano">
        <h3>Mesa individual</h3>
        <p class="para">Para quem quer trabalhar no local</p>
        <div class="preco">R$ 349<small>/mês</small></div>
        <ul>
          <li>Endereço fiscal incluído</li>
          <li>Uso da mesa em horário comercial</li>
          <li>Wi-Fi e recepção para seus clientes</li>
        </ul>
        <a class="botao claro" href="{wa('Olá! Quero saber do plano Mesa individual (R$ 349/mês).')}" target="_blank" rel="noopener" data-origem="{origem}-mesa">Contratar este plano</a>
      </div>
    </div>
    <p class="nota">Temos 10 mesas identificadas na recepção. Antes de contratar, conferimos se a atividade da sua empresa pode usar o endereço.</p>"""


def montar():
    wa_endereco = wa("Olá! Quero saber sobre o endereço fiscal da LG Business.")

    # ---------- Início ----------
    placas = []
    nomes = [("LG Business", "Recepção"), ("Sua empresa", "Mesa 02")]
    placas.append('<li class="placa"><span class="nome">LG Business</span><span class="mesa">Recepção</span></li>')
    placas.append('<li class="placa livre"><span class="nome">Sua empresa</span><span class="mesa">Mesa 02</span></li>')
    for n in range(3, 11):
        placas.append(f'<li class="placa vazia"><span class="mesa">Mesa {n:02d}</span></li>')
    inicio = f"""
<section class="heroi">
  <div class="conteiner">
    <div>
      <h1>Endereço fiscal, salas e gestão no Centro de Bauru.</h1>
      <p class="lead">Sua empresa ganha endereço comercial, mesa com o nome dela e uma equipe de contadores, corretor e advogados no mesmo endereço.</p>
      <div class="acoes">
        <a class="botao whats" href="{wa_endereco}" target="_blank" rel="noopener" data-origem="heroi">Falar no WhatsApp</a>
        <a class="botao claro" href="endereco-fiscal-bauru">Ver planos e preços</a>
      </div>
      <a class="endereco" href="{MAPA}" target="_blank" rel="noopener">{ENDERECO}</a>
    </div>
    <figure class="parede">
      <ul class="placas" aria-label="Mesas identificadas na recepção">
        {"".join(placas)}
      </ul>
      <figcaption>Cada empresa domiciliada tem uma mesa identificada na nossa recepção.</figcaption>
    </figure>
  </div>
</section>

<section class="secao">
  <div class="conteiner">
    <h2>O que você encontra na LG Business</h2>
    <p class="lead">Comece pelo endereço. Quando a empresa crescer, o resto está no mesmo prédio.</p>
    <ul class="areas">
      <li><h3>Endereço fiscal e salas</h3><p>Endereço para o CNPJ a partir de R$ 149/mês, salas privativas com vaga de garagem e sala de reunião por hora.</p><a class="ver" href="endereco-fiscal-bauru">Ver planos</a></li>
      <li><h3>BPO financeiro</h3><p>Contas a pagar e a receber, conciliação bancária e relatórios mensais feitos por quem entende de contabilidade.</p><a class="ver" href="bpo-financeiro">Ver o serviço</a></li>
      <li><h3>Imóveis</h3><p>Compra, venda e administração de aluguéis em Bauru, com corretor CRECI 101.538-F.</p><a class="ver" href="imoveis">Ver imóveis</a></li>
      <li><h3>Compra e venda de empresas</h3><p>Avaliação, preparação e negociação sigilosa para quem quer vender ou comprar um negócio.</p><a class="ver" href="compra-e-venda-de-empresas">Ver o serviço</a></li>
    </ul>
  </div>
</section>

<section class="secao escura">
  <div class="conteiner">
    <h2>Endereço fiscal com preço aberto</h2>
    <p class="lead">Sem orçamento escondido: escolha o plano e fale com a gente.</p>
    {planos_html("inicio")}
  </div>
</section>

<section class="secao">
  <div class="conteiner duas">
    <div>
      <h2>Por que ter a empresa no Centro</h2>
      <ul class="lista-check">
        <li>Endereço conhecido, perto de cartórios, bancos e órgãos públicos.</li>
        <li>Recepção em horário comercial para receber suas correspondências e seus clientes.</li>
        <li>Sua casa fora do cadastro público da empresa.</li>
        <li>Sala de reunião por R$ 150 a hora, com café, quando precisar receber alguém.</li>
      </ul>
    </div>
    <div>
      <h2>Quem atende você</h2>
      <p>A LG Business reúne profissionais registrados nos conselhos de cada área. Você resolve endereço, financeiro, imóveis e contratos sem trocar de endereço.</p>
      <ul class="credenciais" style="grid-template-columns: repeat(2, minmax(0,1fr));">
        <li><strong>CRC</strong><span>Contadores</span></li>
        <li><strong>CRECI</strong><span>Corretor de imóveis</span></li>
        <li><strong>OAB</strong><span>Advogados parceiros</span></li>
        <li><strong>CNAI</strong><span>Avaliador de imóveis</span></li>
      </ul>
    </div>
  </div>
</section>
"""
    pagina("", "LG Business | Endereço fiscal, salas e BPO no Centro de Bauru",
           "Endereço fiscal no Centro de Bauru a partir de R$ 149/mês, salas com vaga de garagem, BPO financeiro, imóveis e compra e venda de empresas.",
           inicio, "inicio")

    # ---------- Endereço fiscal ----------
    endereco = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Endereço fiscal no Centro de Bauru</h1>
    <p class="lead">Use o endereço da LG Business no CNPJ da sua empresa, com mesa identificada e recepção de correspondências. Planos a partir de R$ 149 por mês.</p>
    <div class="acoes">
      <a class="botao whats" href="{wa_endereco}" target="_blank" rel="noopener" data-origem="endereco-topo">Falar no WhatsApp</a>
    </div>
  </div>
</section>

<section class="secao">
  <div class="conteiner">
    <h2>Planos</h2>
    {planos_html("endereco")}
  </div>
</section>

<section class="secao escura">
  <div class="conteiner">
    <h2>Como funciona</h2>
    <ol class="passos">
      <li><h3>Conte sua atividade</h3><p>Pelo WhatsApp, diga o que sua empresa faz. Conferimos se o endereço atende.</p></li>
      <li><h3>Assine o contrato</h3><p>Enviamos o contrato e os documentos do imóvel pedidos no registro.</p></li>
      <li><h3>Atualize o cadastro</h3><p>Seu contador registra o novo endereço na Junta, na Receita e na Prefeitura.</p></li>
      <li><h3>Receba na recepção</h3><p>Sua mesa ganha a placa da empresa e avisamos cada correspondência.</p></li>
    </ol>
  </div>
</section>

<section class="secao">
  <div class="conteiner duas">
    <div>
      <h2>O que está incluído</h2>
      <ul class="lista-check">
        <li>Endereço Rua Gérson França, 6-34, Centro, para o cadastro da empresa</li>
        <li>Mesa identificada com o nome da empresa na recepção</li>
        <li>Recebimento de cartas e encomendas em horário comercial</li>
        <li>Aviso pelo WhatsApp quando chegar correspondência</li>
        <li>Sala de reunião com desconto quando precisar</li>
      </ul>
    </div>
    <div>
      <h2>Peça uma proposta</h2>
      <form class="formulario" data-whats="Olá! Quero contratar o endereço fiscal da LG Business." data-origem="formulario-endereco">
        <label>Seu nome<input name="nome" data-rotulo="Nome" autocomplete="name" required></label>
        <label>O que sua empresa faz<input name="atividade" data-rotulo="Atividade" placeholder="Ex.: consultoria, loja virtual, serviços de TI" required></label>
        <label>Plano de interesse
          <select name="plano" data-rotulo="Plano">
            <option>Endereço fiscal (R$ 149/mês)</option>
            <option>Endereço fiscal comércio (R$ 199/mês)</option>
            <option>Mesa individual (R$ 349/mês)</option>
            <option>Ainda não sei</option>
          </select>
        </label>
        <p class="ajuda">O botão abre o WhatsApp com sua mensagem pronta. Nada fica gravado no site.</p>
        <button class="botao whats" type="submit">Enviar pelo WhatsApp</button>
      </form>
    </div>
  </div>
</section>

<section class="secao">
  <div class="conteiner">
    <h2>Perguntas frequentes</h2>
    <div class="faq">
      <details><summary>Posso usar o endereço para abrir ou mudar o CNPJ?</summary><p>Sim. Antes de contratar, conferimos se a atividade da sua empresa pode funcionar com endereço fiscal pelas regras da Prefeitura de Bauru.</p></details>
      <details><summary>Atendem empresas de comércio com Inscrição Estadual?</summary><p>Sim, pelo plano Endereço fiscal comércio, de R$ 199 por mês.</p></details>
      <details><summary>Como recebo minhas correspondências?</summary><p>A recepção recebe em horário comercial ({HORARIO.lower()}) e avisa você pelo WhatsApp. Você retira na sua mesa.</p></details>
      <details><summary>Posso trabalhar no local?</summary><p>Sim, no plano Mesa individual. Para uma sala só sua, veja as <a href="salas-e-coworking">salas privativas</a>.</p></details>
      <details><summary>Quem cuida da mudança de endereço na Junta e na Receita?</summary><p>O seu contador. Se você não tiver um, nossa equipe contábil pode indicar como fazer.</p></details>
    </div>
  </div>
</section>
"""
    faq_ld = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": "LG Business",
        "telephone": "+55-14-99103-0944", "email": EMAIL, "url": DOMINIO,
        "address": {"@type": "PostalAddress", "streetAddress": "Rua Gérson França, 6-34", "addressLocality": "Bauru",
                    "addressRegion": "SP", "postalCode": "17015-200", "addressCountry": "BR"},
        "openingHours": "Mo-Fr 09:00-17:00",
    }
    ld = '<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False) + "</script>\n"
    pagina("endereco-fiscal-bauru", "Endereço fiscal em Bauru a partir de R$ 149/mês | LG Business",
           "Endereço fiscal e comercial no Centro de Bauru para serviços e comércio, com mesa identificada e recepção de correspondências.",
           endereco, "endereco-fiscal", ld)

    # ---------- Salas ----------
    salas = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Salas e sala de reunião no Centro de Bauru</h1>
    <p class="lead">Cinco salas privativas com vaga de garagem e uma sala de reunião por hora, no mesmo prédio da recepção.</p>
  </div>
</section>

<section class="secao">
  <div class="conteiner">
    <div class="planos" style="grid-template-columns: repeat(2, minmax(0,1fr));">
      <div class="plano destaque">
        <h3>Sala privativa</h3>
        <p class="para">Para quem precisa de escritório próprio</p>
        <div class="preco">R$ 1.250<small>/mês</small></div>
        <ul>
          <li>Sala só sua, com uma vaga de garagem</li>
          <li>Endereço fiscal da empresa incluído</li>
          <li>Recepção para seus clientes e correspondências</li>
        </ul>
        <a class="botao claro" href="{wa('Olá! Quero saber das salas privativas da LG Business (R$ 1.250/mês).')}" target="_blank" rel="noopener" data-origem="sala-privativa">Agendar visita</a>
      </div>
      <div class="plano">
        <h3>Sala de reunião</h3>
        <p class="para">Para receber clientes ou fazer entrevistas</p>
        <div class="preco">R$ 150<small>/hora</small></div>
        <ul>
          <li>Atendimento com café e bolachas</li>
          <li>Reserva pelo WhatsApp</li>
          <li>Clientes de endereço fiscal pagam R$ 120 a hora</li>
        </ul>
        <a class="botao claro" href="{wa('Olá! Quero reservar a sala de reunião da LG Business.')}" target="_blank" rel="noopener" data-origem="sala-reuniao">Reservar horário</a>
      </div>
    </div>
    <p class="nota">Também temos 10 mesas identificadas para quem só precisa de endereço ou de um lugar para trabalhar algumas horas. Veja os <a href="endereco-fiscal-bauru">planos de endereço fiscal</a>.</p>
  </div>
</section>

<section class="secao">
  <div class="conteiner duas">
    <div>
      <h2>Coworking em breve</h2>
      <p>Estamos preparando posições compartilhadas para quem quer trabalhar no Centro alguns dias por semana. Entre na lista e avisamos primeiro.</p>
      <div class="acoes"><a class="botao claro" href="{wa('Olá! Quero entrar na lista de espera do coworking da LG Business.')}" target="_blank" rel="noopener" data-origem="coworking">Entrar na lista</a></div>
    </div>
    <div>
      <h2>Visite antes de decidir</h2>
      <p>{ENDERECO}<br>{HORARIO}.</p>
      <p><a href="{MAPA}" target="_blank" rel="noopener">Abrir no Google Maps</a></p>
    </div>
  </div>
</section>
"""
    pagina("salas-e-coworking", "Salas comerciais e sala de reunião no Centro de Bauru | LG Business",
           "Salas privativas com vaga de garagem por R$ 1.250/mês e sala de reunião por R$ 150/hora no Centro de Bauru.",
           salas, "salas")

    # ---------- BPO financeiro ----------
    bpo = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>BPO financeiro para pequenas empresas</h1>
    <p class="lead">Nossa equipe cuida da rotina financeira da sua empresa e entrega todo mês os números para você decidir.</p>
    <div class="acoes"><a class="botao whats" href="{wa('Olá! Quero conversar sobre o BPO financeiro da LG Business.')}" target="_blank" rel="noopener" data-origem="bpo-topo">Agendar uma conversa</a></div>
  </div>
</section>

<section class="secao">
  <div class="conteiner duas">
    <div>
      <h2>O que fazemos por você</h2>
      <ul class="lista-check">
        <li>Contas a pagar e a receber</li>
        <li>Conciliação bancária</li>
        <li>Fluxo de caixa atualizado</li>
        <li>Relatório mensal com receitas, despesas e resultado</li>
        <li>Organização dos documentos para o seu contador</li>
      </ul>
    </div>
    <div>
      <h2>Para quem é</h2>
      <p>Para donos de pequenas empresas que perdem horas com boletos e planilhas, ou que não sabem quanto a empresa realmente ganha no mês.</p>
      <p>Clientes de endereço fiscal da LG Business já estão no mesmo prédio da equipe que faz o serviço.</p>
    </div>
  </div>
</section>

<section class="secao escura">
  <div class="conteiner">
    <h2>Como começamos</h2>
    <ol class="passos">
      <li><h3>Conversa inicial</h3><p>Entendemos como o financeiro da empresa funciona hoje.</p></li>
      <li><h3>Proposta</h3><p>Você recebe o escopo e o valor mensal por escrito.</p></li>
      <li><h3>Organização</h3><p>Montamos as rotinas e acessos com você.</p></li>
      <li><h3>Rotina mensal</h3><p>Cuidamos do dia a dia e enviamos o relatório todo mês.</p></li>
    </ol>
  </div>
</section>
"""
    pagina("bpo-financeiro", "BPO financeiro em Bauru | LG Business",
           "Terceirize o financeiro da sua empresa: contas a pagar e a receber, conciliação bancária, fluxo de caixa e relatórios mensais em Bauru.",
           bpo, "bpo")

    # ---------- Imóveis ----------
    imoveis = []
    with open(os.path.join(RAIZ, "_build", "imoveis.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            def num(v):
                return int(v) if v else None
            imoveis.append({
                "finalidade": r["finalidade"], "tipo": r["tipo"], "bairro": r["bairro"],
                "dormitorios": num(r["dormitorios"]), "suites": num(r["suites"]), "garagens": num(r["garagens"]),
                "venda": num(r["preco_venda"]), "locacao": num(r["preco_locacao"]),
            })
    dados = "<script>window.IMOVEIS = " + json.dumps(imoveis, ensure_ascii=False) + ";</script>\n"
    tipos = sorted({i["tipo"] for i in imoveis})
    botoes_tipo = "".join(
        f'<button type="button" data-grupo="tipo" data-valor="{t}" aria-pressed="false">{t}</button>' for t in tipos)
    imv = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Imóveis em Bauru</h1>
    <p class="lead">Casas, apartamentos, salões e terrenos para comprar ou alugar, com corretor responsável Nelson de Castro Ramos Neto, CRECI 101.538-F.</p>
  </div>
</section>

<section class="secao" style="padding-top:0">
  <div class="conteiner">
    <div class="filtros" role="group" aria-label="Finalidade">
      <button type="button" data-grupo="finalidade" data-valor="todos" aria-pressed="true">Todos</button>
      <button type="button" data-grupo="finalidade" data-valor="venda" aria-pressed="false">Comprar</button>
      <button type="button" data-grupo="finalidade" data-valor="locacao" aria-pressed="false">Alugar</button>
    </div>
    <div class="filtros" role="group" aria-label="Tipo de imóvel">
      <button type="button" data-grupo="tipo" data-valor="todos" aria-pressed="true">Todos os tipos</button>
      {botoes_tipo}
    </div>
    <p class="contagem" id="contagem-imoveis" aria-live="polite"></p>
    <ul class="imoveis" id="lista-imoveis"></ul>
    <p class="nota">Peça fotos, endereço e condições pelo WhatsApp. Valores sujeitos a alteração sem aviso.</p>
  </div>
</section>

<section class="secao escura">
  <div class="conteiner duas">
    <div>
      <h2>Administração de aluguéis</h2>
      <p>Para proprietários que querem renda sem dor de cabeça: anunciamos, escolhemos o inquilino, cuidamos do contrato, da cobrança e das vistorias.</p>
      <div class="acoes"><a class="botao whats" href="{wa('Olá! Tenho um imóvel e quero saber da administração de aluguel da LG Business.')}" target="_blank" rel="noopener" data-origem="administracao">Falar sobre meu imóvel</a></div>
    </div>
    <div>
      <h2>Quer vender seu imóvel?</h2>
      <p>Avaliamos o preço de mercado e cuidamos da divulgação e da negociação até a escritura.</p>
      <div class="acoes"><a class="botao claro" style="color:#fff;border-color:#fff" href="{wa('Olá! Quero vender meu imóvel com a LG Business.')}" target="_blank" rel="noopener" data-origem="vender-imovel">Avaliar meu imóvel</a></div>
    </div>
  </div>
</section>
"""
    pagina("imoveis", "Imóveis à venda e para alugar em Bauru | LG Business",
           "Casas, apartamentos, salões e terrenos à venda e para alugar em Bauru. Administração de aluguéis com corretor CRECI 101.538-F.",
           imv, "imoveis", dados)

    # ---------- M&A ----------
    ma = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Compra e venda de empresas</h1>
    <p class="lead">Assessoria para vender ou comprar um negócio com segurança: do valor da empresa à assinatura do contrato, com sigilo em todas as etapas.</p>
    <div class="acoes"><a class="botao whats" href="{wa('Olá! Quero uma conversa sigilosa sobre compra ou venda de empresa.')}" target="_blank" rel="noopener" data-origem="ma-topo">Marcar conversa sigilosa</a></div>
  </div>
</section>

<section class="secao">
  <div class="conteiner">
    <h2>Como conduzimos uma venda</h2>
    <ol class="passos">
      <li><h3>Avaliação</h3><p>Estimamos quanto vale a empresa a partir dos números e do mercado.</p></li>
      <li><h3>Preparação</h3><p>Organizamos documentos e corrigimos o que pode afastar compradores.</p></li>
      <li><h3>Busca e negociação</h3><p>Apresentamos a empresa só a interessados que assinam termo de sigilo.</p></li>
      <li><h3>Contrato</h3><p>Advogados parceiros acompanham a análise e o contrato até a assinatura.</p></li>
    </ol>
  </div>
</section>

<section class="secao escura">
  <div class="conteiner duas">
    <div>
      <h2>Para quem está comprando</h2>
      <p>Ajudamos a encontrar negócios à venda, a conferir os números e a negociar preço e condições.</p>
    </div>
    <div>
      <h2>Depois da negociação</h2>
      <p>O novo dono pode contar com nosso BPO financeiro e com o endereço fiscal no Centro na transição.</p>
    </div>
  </div>
</section>
"""
    pagina("compra-e-venda-de-empresas", "Compra e venda de empresas em Bauru | LG Business",
           "Assessoria sigilosa para comprar ou vender empresas em Bauru e região: avaliação, preparação, negociação e contrato.",
           ma, "ma")

    # ---------- Contato ----------
    contato = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Fale com a LG Business</h1>
    <p class="lead">Atendemos pelo WhatsApp, por e-mail ou pessoalmente no Centro de Bauru.</p>
  </div>
</section>
<section class="secao" style="padding-top:0">
  <div class="conteiner duas">
    <div>
      <ul class="lista-check">
        <li><a href="{wa('Olá! Vim pelo site da LG Business.')}" target="_blank" rel="noopener" data-origem="contato">WhatsApp {FONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{MAPA}" target="_blank" rel="noopener">{ENDERECO}</a></li>
        <li>{HORARIO}</li>
      </ul>
    </div>
    <div>
      <form class="formulario" data-whats="Olá! Vim pelo site da LG Business." data-origem="formulario-contato">
        <label>Seu nome<input name="nome" data-rotulo="Nome" autocomplete="name" required></label>
        <label>Assunto
          <select name="assunto" data-rotulo="Assunto">
            <option>Endereço fiscal</option>
            <option>Salas e sala de reunião</option>
            <option>BPO financeiro</option>
            <option>Imóveis</option>
            <option>Compra e venda de empresas</option>
            <option>Outro assunto</option>
          </select>
        </label>
        <label>Mensagem<textarea name="mensagem" data-rotulo="Mensagem"></textarea></label>
        <p class="ajuda">O botão abre o WhatsApp com sua mensagem pronta. Nada fica gravado no site.</p>
        <button class="botao whats" type="submit">Enviar pelo WhatsApp</button>
      </form>
    </div>
  </div>
</section>
"""
    pagina("contato", "Contato | LG Business Bauru",
           "WhatsApp (14) 99103-0944, atendimento@lgbusiness.adm.br e endereço na Rua Gérson França, 6-34, Centro, Bauru.",
           contato, "contato")

    # ---------- Privacidade ----------
    priv = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Política de privacidade</h1>
    <p>Esta página explica como a L.G. Business Ltda. (CNPJ 08.468.684/0001-62) trata dados pessoais neste site, conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018).</p>
    <h2>Dados que recebemos</h2>
    <p>O site não grava os dados digitados nos formulários. Ao clicar em enviar, o WhatsApp abre com a sua mensagem, e só a recebemos se você decidir enviá-la. Usamos o que você nos enviar apenas para responder e prestar o serviço pedido.</p>
    <h2>Cookies e medição</h2>
    <p>Se você aceitar no aviso de cookies, usamos ferramentas do Google e da Meta para medir visitas e saber quais anúncios trazem contatos. Se recusar, essas ferramentas não são carregadas. Você pode mudar a escolha limpando os dados do site no seu navegador.</p>
    <h2>Seus direitos</h2>
    <p>Você pode pedir acesso, correção ou exclusão dos seus dados pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>
"""
    pagina("politica-de-privacidade", "Política de privacidade | LG Business",
           "Como a LG Business trata dados pessoais neste site.", priv, "privacidade")

    # ---------- 404 ----------
    p404 = f"""
<section class="cabeca-pagina">
  <div class="conteiner">
    <h1>Esta página mudou de endereço</h1>
    <p class="lead">O site da LG Business foi renovado. Escolha uma área no menu ou fale com a gente pelo WhatsApp.</p>
    <div class="acoes"><a class="botao" href="./">Ir para o início</a></div>
  </div>
</section>
"""
    base404 = ("<script>(function(){var b=location.pathname.indexOf('/lgbusiness-site/')===0?'/lgbusiness-site/':'/';"
               "document.write('<base href=\\''+b+'\\'>');"
               "var m={'site/conteudo/bpo':'bpo-financeiro','site/conteudo/m-a':'compra-e-venda-de-empresas',"
               "'site/conteudo/parceiros-profissionais':'','estrutura-organizacional':'','site/imoveis':'imoveis'};"
               "var p=location.pathname.slice(b.length).replace(/\\/$/,'');"
               "if(Object.prototype.hasOwnProperty.call(m,p)){location.replace(b+m[p]);}})();</script>\n")
    pagina("404", "Página não encontrada | LG Business", "Página não encontrada.", p404, "404", base404)

    # ---------- robots e sitemap ----------
    with open(os.path.join(RAIZ, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    urls = ["", "endereco-fiscal-bauru", "salas-e-coworking", "bpo-financeiro", "imoveis",
            "compra-e-venda-de-empresas", "contato", "politica-de-privacidade"]
    with open(os.path.join(RAIZ, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{DOMINIO}/{u}</loc></url>\n")
        f.write("</urlset>\n")


if __name__ == "__main__":
    montar()
    print("Site gerado.")
