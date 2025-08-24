# File Organizer

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)
![Status](https://img.shields.io/badge/status-active-success?style=flat-square)

**Um organizador automático de arquivos inteligente com interface gráfica e monitoramento em tempo real**

[Instalação](#instalação) • [Uso](#como-usar) • [Configuração](#configuração) • [Contribuição](#contribuição)

</div>

---

## Visão Geral

O **File Organizer** é uma ferramenta Python que automatiza a organização de arquivos em pastas com base em regras personalizáveis. Ideal para manter diretórios como Downloads, Desktop ou pastas de trabalho sempre organizados.

### Principais Funcionalidades

- **Interface Gráfica Intuitiva**: Aplicação desktop completa com Tkinter
- **Organização por Tipo**: Classifica automaticamente por extensão de arquivo
- **Organização por Data**: Cria estruturas baseadas na data de modificação
- **Monitoramento em Tempo Real**: Organiza novos arquivos automaticamente
- **Configuração Flexível**: Regras totalmente personalizáveis via JSON
- **Log Detalhado**: Registro completo de todas as operações

---

## Instalação

### Pré-requisitos

- Python 3.7 ou superior
- Tkinter (geralmente incluído com Python)

### Instalação Básica

```bash
# Clone o repositório
git clone https://github.com/NullCeu/auto-organizer
cd file-organizer

# Execute diretamente
python organizador_arquivos.py
```

### Instalação com Monitoramento em Tempo Real

Para habilitar o monitoramento automático de pastas:

```bash
pip install watchdog
```

### Dependências Opcionais

```bash
# Para funcionalidades completas
pip install -r requirements.txt
```

---

## Como Usar

### Iniciando o Programa

```bash
python organizador_arquivos.py
```

### Interface Principal

1. **Seleção de Pasta**: Clique em "Procurar" para escolher a pasta a ser organizada
2. **Organização Imediata**: Use "Organizar Agora" para processar todos os arquivos
3. **Monitoramento**: Ative "Iniciar Monitoramento" para organização automática
4. **Configurações**: Acesse "Configurações" para personalizar regras

### Exemplo de Uso Rápido

```bash
# 1. Execute o programa
python organizador_arquivos.py

# 2. Selecione sua pasta Downloads
# 3. Clique em "Organizar Agora"
# 4. Ative o monitoramento para organização automática
```

---

## Estrutura de Organização

### Organização por Tipo (Padrão)

```
Downloads/
├── 📸 Imagens/
│   ├── foto1.jpg
│   ├── screenshot.png
│   └── avatar.gif
├── 📄 Documentos/
│   ├── relatorio.pdf
│   ├── planilha.xlsx
│   └── apresentacao.pptx
├── 🎵 Áudio/
│   ├── musica.mp3
│   └── podcast.wav
├── 🎬 Vídeos/
│   └── filme.mp4
├── 💻 Código/
│   ├── script.py
│   ├── website.html
│   └── styles.css
└── 📁 Outros/
    └── arquivo_desconhecido.xyz
```

### Organização por Data

Quando habilitada a organização por data:

```
Downloads/
├── 2024-08/
│   ├── 📸 Imagens/
│   └── 📄 Documentos/
├── 2024-09/
│   ├── 🎵 Áudio/
│   └── 💻 Código/
└── 2024-10/
    └── 📁 Outros/
```

---

## Configuração

### Arquivo de Configuração

O programa cria automaticamente um arquivo `organizer_config.json` com as seguintes opções:

```json
{
  "rules": {
    "images": {
      "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
      "folder": "📸 Imagens"
    },
    "documents": {
      "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
      "folder": "📄 Documentos"
    }
  },
  "organize_by_date": false,
  "date_format": "%Y-%m",
  "ignore_hidden": true
}
```

### Tipos de Arquivo Suportados

| Categoria | Extensões | Pasta Destino |
|-----------|-----------|---------------|
| **Imagens** | .jpg, .png, .gif, .bmp, .svg, .webp | 📸 Imagens |
| **Documentos** | .pdf, .doc, .docx, .txt, .xlsx, .ppt | 📄 Documentos |
| **Áudio** | .mp3, .wav, .flac, .aac, .m4a, .ogg | 🎵 Áudio |
| **Vídeo** | .mp4, .avi, .mkv, .mov, .wmv, .webm | 🎬 Vídeos |
| **Código** | .py, .js, .html, .css, .cpp, .java | 💻 Código |
| **Arquivos** | .zip, .rar, .7z, .tar, .gz | 📦 Arquivos Compactados |
| **Executáveis** | .exe, .msi, .deb, .rpm, .dmg | ⚙️ Executáveis |

### Formatos de Data

| Formato | Exemplo | Descrição |
|---------|---------|-----------|
| `%Y-%m` | `2024-08` | Ano-Mês |
| `%Y-%m-%d` | `2024-08-24` | Ano-Mês-Dia |
| `%Y` | `2024` | Apenas Ano |
| `%Y-Q%q` | `2024-Q3` | Ano-Trimestre |

### Personalizando Regras

#### Adicionando Novo Tipo de Arquivo

```json
{
  "rules": {
    "ebooks": {
      "extensions": [".epub", ".mobi", ".azw", ".azw3"],
      "folder": "📚 E-books"
    }
  }
}
```

#### Modificando Pastas Existentes

```json
{
  "rules": {
    "images": {
      "extensions": [".jpg", ".png"],
      "folder": "Minhas_Fotos"
    }
  }
}
```

---

## Funcionalidades Avançadas

### Monitoramento em Tempo Real

O sistema utiliza a biblioteca `watchdog` para detectar automaticamente:

- Novos arquivos adicionados à pasta
- Downloads concluídos
- Arquivos movidos para a pasta monitorada

#### Configuração do Monitoramento

```python
# O monitoramento é configurado automaticamente
# Aguarda 1 segundo após detecção para garantir que o arquivo foi completamente copiado
```

### Sistema de Log

O programa mantém um log detalhado de todas as operações:

```
[14:23:15] 🚀 Organizador de Arquivos iniciado!
[14:23:32] 📁 Pasta selecionada: /Users/usuario/Downloads
[14:23:35] 🔄 Iniciando organização da pasta: /Users/usuario/Downloads
[14:23:35] ✅ documento.pdf → 📄 Documentos/documento.pdf
[14:23:35] ✅ musica.mp3 → 🎵 Áudio/musica.mp3
[14:23:36] 📊 Resumo: 15 arquivos organizados, 0 erros
```

### Resolução de Conflitos

Quando arquivos com o mesmo nome já existem:

```
arquivo.pdf → arquivo_1.pdf
arquivo.pdf → arquivo_2.pdf
```

---

## API e Uso Programático

### Uso Básico em Script

```python
from organizador_arquivos import FileOrganizer

# Criar instância do organizador
organizer = FileOrganizer()

# Organizar uma pasta específica
success, message = organizer.organize_folder("/caminho/para/pasta")

if success:
    print("Organização concluída com sucesso!")
else:
    print(f"Erro: {message}")
```

### Organizando Arquivo Específico

```python
# Organizar apenas um arquivo
success, message = organizer.organize_file(
    "/caminho/arquivo.pdf", 
    "/pasta/destino"
)
```

### Configuração Programática

```python
# Modificar configurações via código
organizer.config["organize_by_date"] = True
organizer.config["date_format"] = "%Y-%m-%d"
organizer.save_config()
```

---

## Solução de Problemas

### Problemas Comuns

#### Watchdog não instalado
```
⚠️ Watchdog não instalado. Monitoramento em tempo real indisponível.
Para instalar: pip install watchdog
```

**Solução:**
```bash
pip install watchdog
```

#### Permissões de arquivo
```
❌ Erro ao mover arquivo.txt: [Errno 13] Permission denied
```

**Solução:**
- Execute como administrador/root
- Verifique permissões da pasta
- Certifique-se que o arquivo não está em uso

#### Pasta não encontrada
```
❌ Pasta não encontrada
```

**Solução:**
- Verifique se o caminho existe
- Use caminhos absolutos
- Certifique-se que tem acesso à pasta

### Performance

Para otimizar a performance em pastas grandes:

```json
{
  "ignore_hidden": true,
  "organize_by_date": false
}
```

---

## Desenvolvimento

### Estrutura do Projeto

```
file-organizer/
├── organizador_arquivos.py    # Arquivo principal
├── organizer_config.json      # Configurações (gerado automaticamente)
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências
├── LICENSE                    # Licença MIT
└── tests/                     # Testes unitários (futuro)
```

### Classes Principais

- **`FileOrganizer`**: Lógica principal de organização
- **`FileWatcher`**: Handler para monitoramento em tempo real
- **`OrganizerGUI`**: Interface gráfica principal
- **`ConfigWindow`**: Janela de configurações

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

#### Diretrizes de Contribuição

- Mantenha o código Python 3.7+ compatível
- Adicione testes para novas funcionalidades
- Mantenha a documentação atualizada
- Use type hints quando possível
- Siga PEP 8 para estilo de código

---

## Roadmap

### Próximas Versões

- [ ] **v2.0**: Suporte a regras baseadas em tamanho de arquivo
- [ ] **v2.1**: Integração com serviços de nuvem
- [ ] **v2.2**: Sistema de plugins
- [ ] **v2.3**: Interface web opcional
- [ ] **v2.4**: Suporte a expressões regulares em nomes
- [ ] **v2.5**: Organização por metadados (EXIF, tags de música)

### Funcionalidades Planejadas

- **Desfazer Operações**: Capacidade de reverter organizações
- **Backup Automático**: Backup antes de grandes reorganizações
- **Relatórios**: Estatísticas detalhadas de uso
- **Temas**: Interface personalizável
- **CLI Avançada**: Versão linha de comando completa

---

## FAQ

### Perguntas Frequentes

**Q: O programa move ou copia os arquivos?**
A: O programa **move** os arquivos por padrão, mantendo apenas uma cópia.

**Q: É seguro usar em arquivos importantes?**
A: Sim, mas recomendamos testar primeiro em uma pasta pequena. O programa inclui resolução de conflitos.

**Q: Posso desfazer uma organização?**
A: Atualmente não há função de desfazer automática. Mantenha backups importantes.

**Q: Funciona em rede/pastas compartilhadas?**
A: Sim, funciona com qualquer pasta acessível pelo sistema operacional.

**Q: Quantos arquivos pode processar?**
A: Não há limite teórico. Testado com milhares de arquivos.

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Créditos

Desenvolvido com ❤️ usando:

- **Python**: Linguagem principal
- **Tkinter**: Interface gráfica
- **Watchdog**: Monitoramento de sistema de arquivos
- **JSON**: Configurações

---

## Suporte

### Como Obter Ajuda

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/file-organizer/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/file-organizer/discussions)
- **Email**: seu-email@example.com

### Reportando Bugs

Ao reportar bugs, inclua:

1. Versão do Python
2. Sistema operacional
3. Passos para reproduzir
4. Mensagens de erro completas
5. Configuração usada (organizer_config.json)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

[⬆ Voltar ao topo](#file-organizer)

</div>
