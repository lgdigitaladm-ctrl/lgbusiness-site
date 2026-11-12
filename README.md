# lgbusiness-site

Site da LG Business — lgbusiness.adm.br.

- Textos e páginas: `_build/build.py`. Depois de editar, rode `python3 _build/build.py` na raiz para gerar os arquivos HTML.
- Imóveis: `_build/imoveis.json` (ref, dados, descrição, quantidade de fotos). Fotos em `fotos-imoveis/{ref}/` (`1.jpg` grande, `{n}-p.jpg` miniatura). Cada imóvel gera uma página `imovel-{ref}-...html`.
- Visual e comportamento: `site.css` e `site.js`. Os códigos de medição (GA4, Google Ads, Pixel da Meta) ficam no início de `site.js`.
- Hospedagem: GitHub Pages, branch `main`, pasta raiz. O domínio próprio é configurado só quando o DNS for apontado.
