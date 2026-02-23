### Estapas Workflow:

- 1. Crie o arquivo VERSION na raiz do repo
- Na raiz project_yt_videos_leg/, crie o arquivo VERSION (sem extensão) com: '2.0.0' escrito nele

```
gui.spec e gui.py dentro de yt_leg/
requeriments.txt na raiz (mantive o seu nome com esse typo mesmo)
build no Windows, zipando yt_leg/dist/ e criando Release
PR dev → main automático + auto-merge habilitado
versão lida do arquivo VERSION na raiz (texto puro)
```

- 2. Crie: .github/workflows/pr-dev-to-main.yml
- 3. Crie: .github/workflows/ci.yml (check obrigatório para liberar auto-merge)
*Crie esse arquivo (simples, só pra existir um status check obrigatório)*
- 4. .github/workflows/release-on-merge.yml
*Esse é o principal: ao merge do PR dev → main ele cria tag v2.0.0, builda via yt_leg/gui.spec, zipa yt_leg/dist, cria release e anexa o zip.*


O fluxo:

- Para só atualizar a main (sem release)
- faz commits na dev
- não mexe no VERSION
- push → PR abre → auto-merge → workflow roda e pula release

**Dispara ao soltar uma release (ex.: v2.0.0)**

- Na dev, altere o arquivo VERSION para 2.0.0, commit e push.
- No merge, o workflow vai:
       - criar tag v2.0.0
       - buildar pelo yt_leg/gui.spec
       - criar Release com o zip anexado

### Liberar as permissões no GitHub Web para que o pipeline funcione:

- **Habilitar Auto-Merge**
    - Vá no seu repositório no GitHub
    - Clique em Settings
    - No menu lateral clique em General
    - Role até a seção Pull Requests
    - Marque: Allow auto-merge
    - Clique em Save (se aparecer)

- **Liberar permissões do GitHub Actions**

> Isso é ESSENCIAL para que ele consiga:

   - Criar PR
   - Criar tag
   - Criar release
   - Caminho:
        - Settings
        - Clique em Actions
        - Clique em General

- **Na seção Workflow permissions, selecione:**

- Read and write permissions
- E marque também Allow GitHub Actions to create and approve pull requests
- Clique em Save    

- Proteger a branch main:

> Isso é obrigatório para o auto-merge funcionar corretamente.

- Caminho:
    - Settings
    - Clique em Branches
    - Clique em Add branch protection rule
    - Preencha: `main`

Marque:

- Require a pull request before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging

**Depois de marcar "Require status checks" clique em Search for status checks e Selecione:**

`CI / smoke` Obs: (é o workflow que criamos)

Clique em `Create`

### Resultado final esperado:

Quando fizer o `git push` na branch `dev`:

- 1. Pull Requests abre automaticamente
- 2. CI roda
- 3. Auto-merge acontece
    - 3.1. Merge dispara:
        - 3.1.1. leitura do VERSION
        - 3.1.2. criação da tag v2.0.0
        - 3.1.3. build do .exe
        - 3.1.4. criação da Release

Tudo automático.

### Última verificação importante:

Depois de configurar tudo:

- Vá na aba `Actions` e confirme que Workflows aparecem e sem erros de permissão.

Se aparecer erro tipo: `Resource not accessible by integration`

É quase sempre porque você esqueceu de ativar: `Read and write permissions`





