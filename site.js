/* LG Business — comportamento do site */
(function () {
  "use strict";

  // Preencha quando as contas de medição estiverem prontas.
  // Ex.: GA4 "G-XXXXXXX", Google Ads "AW-XXXXXXX", Pixel da Meta "123456789".
  var MEDICAO = { ga4: "", googleAds: "", metaPixel: "" };
  var WHATS = "5514991030944";

  function lerConsentimento() {
    try { return localStorage.getItem("lg-consentimento"); } catch (e) { return null; }
  }
  function gravarConsentimento(v) {
    try { localStorage.setItem("lg-consentimento", v); } catch (e) { /* sem armazenamento */ }
  }

  function carregarMedicao() {
    if (MEDICAO.ga4 || MEDICAO.googleAds) {
      var id = MEDICAO.ga4 || MEDICAO.googleAds;
      var s = document.createElement("script");
      s.async = true;
      s.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      if (MEDICAO.ga4) window.gtag("config", MEDICAO.ga4);
      if (MEDICAO.googleAds) window.gtag("config", MEDICAO.googleAds);
    }
    if (MEDICAO.metaPixel) {
      /* eslint-disable */
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");
      /* eslint-enable */
      window.fbq("init", MEDICAO.metaPixel);
      window.fbq("track", "PageView");
    }
  }

  function avisoCookies() {
    var temMedicao = MEDICAO.ga4 || MEDICAO.googleAds || MEDICAO.metaPixel;
    if (!temMedicao) return;
    var escolha = lerConsentimento();
    if (escolha === "aceito") { carregarMedicao(); return; }
    if (escolha === "recusado") return;
    var raiz = document.body.getAttribute("data-raiz") || "";
    var caixa = document.createElement("div");
    caixa.className = "aviso-cookies";
    caixa.setAttribute("role", "dialog");
    caixa.setAttribute("aria-label", "Uso de cookies");
    caixa.innerHTML =
      '<p>Usamos cookies de medição para saber quais anúncios trazem contatos. Veja a <a href="' + raiz + 'politica-de-privacidade">política de privacidade</a>.</p>' +
      '<div class="acoes"><button type="button" class="botao" data-c="aceito">Aceitar</button>' +
      '<button type="button" class="botao claro" data-c="recusado">Recusar</button></div>';
    caixa.addEventListener("click", function (ev) {
      var v = ev.target.getAttribute("data-c");
      if (!v) return;
      gravarConsentimento(v);
      if (v === "aceito") carregarMedicao();
      caixa.remove();
    });
    document.body.appendChild(caixa);
  }

  function registrarContato(origem) {
    if (window.gtag) {
      window.gtag("event", "generate_lead", { method: "whatsapp", origem: origem });
      if (MEDICAO.googleAds) window.gtag("event", "conversion", { send_to: MEDICAO.googleAds });
    }
    if (window.fbq) window.fbq("track", "Contact", { origem: origem });
  }

  function linkWhats(texto) {
    return "https://wa.me/" + WHATS + "?text=" + encodeURIComponent(texto);
  }

  // Menu no celular
  var botaoMenu = document.querySelector(".botao-menu");
  var menu = document.getElementById("menu");
  if (botaoMenu && menu) {
    botaoMenu.addEventListener("click", function () {
      var aberto = menu.classList.toggle("aberto");
      botaoMenu.setAttribute("aria-expanded", aberto ? "true" : "false");
    });
  }

  // Cliques em WhatsApp contam como contato
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="https://wa.me/"]');
    if (a) registrarContato(a.getAttribute("data-origem") || document.body.getAttribute("data-pagina") || "site");
  });

  // Formulários que montam a mensagem e abrem o WhatsApp (nada é gravado no site)
  Array.prototype.forEach.call(document.querySelectorAll("form[data-whats]"), function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var linhas = [form.getAttribute("data-whats")];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || !el.value) return;
        var rotulo = el.getAttribute("data-rotulo") || el.name;
        linhas.push(rotulo + ": " + el.value);
      });
      registrarContato(form.getAttribute("data-origem") || "formulario");
      window.open(linkWhats(linhas.join("\n")), "_blank", "noopener");
    });
  });

  // Lista de imóveis
  var lista = document.getElementById("lista-imoveis");
  if (lista && window.IMOVEIS) {
    var estado = { finalidade: "todos", tipo: "todos" };
    var contagem = document.getElementById("contagem-imoveis");
    var moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });

    function detalhes(i) {
      var d = [];
      if (i.dormitorios) d.push(i.dormitorios + (i.dormitorios === 1 ? " dormitório" : " dormitórios"));
      if (i.suites) d.push(i.suites + (i.suites === 1 ? " suíte" : " suítes"));
      if (i.garagens) d.push(i.garagens + (i.garagens === 1 ? " vaga" : " vagas"));
      return d.join(", ");
    }
    function valor(i) {
      var partes = [];
      if (i.venda) partes.push(moeda.format(i.venda) + "<small>venda</small>");
      if (i.locacao) partes.push(moeda.format(i.locacao) + "<small>aluguel por mês</small>");
      return partes.length ? partes.join("") : "Sob consulta";
    }
    function confere(i) {
      var f = estado.finalidade;
      var okFin = f === "todos" || (f === "venda" && i.venda) || (f === "locacao" && i.locacao) ||
        (f === "locacao" && i.finalidade === "Locação");
      var okTipo = estado.tipo === "todos" || i.tipo === estado.tipo;
      return okFin && okTipo;
    }
    function desenhar() {
      var itens = window.IMOVEIS.filter(confere);
      contagem.textContent = itens.length === 1 ? "1 imóvel" : itens.length + " imóveis";
      if (!itens.length) {
        lista.innerHTML = '<li class="imovel"><span>Nenhum imóvel com esse filtro agora. Fale com a gente pelo WhatsApp e avisamos quando entrar um.</span></li>';
        return;
      }
      lista.innerHTML = itens.map(function (i) {
        var bairro = i.bairro || "Bauru";
        var msg = "Olá! Tenho interesse no imóvel: " + i.tipo + " em " + bairro + " (" + i.finalidade.toLowerCase() + "). Pode me enviar fotos e detalhes?";
        return '<li class="imovel">' +
          '<div class="col-tipo"><span class="tipo">' + i.tipo + '</span><span class="fin">' + i.finalidade + '</span></div>' +
          '<div><span class="bairro">' + bairro + '</span><span class="det">' + (detalhes(i) || "Bauru, SP") + '</span></div>' +
          '<div class="valor">' + valor(i) + '</div>' +
          '<a href="' + linkWhats(msg) + '" target="_blank" rel="noopener" data-origem="imovel">Pedir fotos</a>' +
          '</li>';
      }).join("");
    }
    Array.prototype.forEach.call(document.querySelectorAll(".filtros button"), function (b) {
      b.addEventListener("click", function () {
        var grupo = b.getAttribute("data-grupo");
        estado[grupo] = b.getAttribute("data-valor");
        Array.prototype.forEach.call(document.querySelectorAll('.filtros button[data-grupo="' + grupo + '"]'), function (o) {
          o.setAttribute("aria-pressed", o === b ? "true" : "false");
        });
        desenhar();
      });
    });
    desenhar();
  }

  avisoCookies();
})();
