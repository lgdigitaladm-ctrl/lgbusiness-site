# lgbusiness-site

Site da LG Business — lgbusiness.adm.br.

- Textos e páginas: `_build/build.py`. Depois de editar, rode `python3 _build/build.py` na raiz para gerar os arquivos HTML.
- Imóveis: `_build/imoveis.csv` (uma linha por imóvel; preços sem pontos).
- Visual e comportamento: `assets/site.css` e `assets/site.js`. Os códigos de medição (GA4, Google Ads, Pixel da Meta) ficam no início de `assets/site.js`.
- Hospedagem: GitHub Pages, branch `main`, pasta raiz. O domínio próprio é configurado só quando o DNS for apontado.
