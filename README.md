# Gravador de Voz Discreto para Windows

Um aplicativo simples para Windows que permite gravar áudio do microfone de forma discreta, operando exclusivamente a partir da bandeja do sistema (system tray).

## Funcionalidades

- **Operação Discreta:** Sem janela principal, ícone na barra de tarefas ou visibilidade no Alt+Tab.
- **Controle pela Bandeja do Sistema:** O aplicativo é controlado por um ícone na bandeja do sistema (ao lado do relógio), com um menu de clique com o botão direito.
- **Fácil de Usar:** Opções simples para "Iniciar Gravação", "Parar Gravação" e "Sair".
- **Salvamento Automático:** As gravações são salvas automaticamente em formato `.wav` na pasta `recordings/`, com o nome do arquivo sendo a data e a hora da gravação (ex: `2025-08-29_14-30-00.wav`).

## Pré-requisitos

Para executar o projeto a partir do código-fonte, você precisará ter o Python 3 instalado em seu sistema.

## Instalação e Configuração (para Desenvolvedores)

Se você deseja executar ou modificar o projeto a partir do código-fonte, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_AQUI>
    cd voice-recorder
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    As dependências estão listadas no arquivo `requirements.txt` (que criaremos a seguir). Por enquanto, você pode instalá-las manualmente:
    ```bash
    pip install pystray Pillow sounddevice numpy wavio
    ```

## Como Usar

### A partir do Código-Fonte

Após a instalação das dependências, execute o script principal:

```bash
python src/main.py
```

Um ícone de microfone aparecerá na sua bandeja do sistema. Clique com o botão direito nele para controlar a gravação.

### Usando o Executável (`.exe`)

Para conveniência, um arquivo `VoiceRecorder.exe` pode ser gerado. Ele pode ser executado em qualquer máquina Windows sem a necessidade de instalar Python ou qualquer dependência.

1.  Navegue até a pasta `dist/`.
2.  Execute o arquivo `VoiceRecorder.exe`.
3.  O ícone aparecerá na bandeja do sistema, pronto para uso.
