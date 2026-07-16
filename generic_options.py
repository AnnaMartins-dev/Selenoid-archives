from pathlib import Path
from typing import Optional

from selenium.webdriver.chrome.options import Options


def add_selenoid_options(
    options: Options,
    *,
    browser_version: str = "149.0",
    enable_vnc: bool = True,
    enable_log: bool = True,
    enable_video: bool = False,
    log_name: Optional[str] = None,
    video_name: Optional[str] = None,
    session_name: Optional[str] = None,
    screen_resolution: str = "1280x720x24",
    timezone: str = "America/Sao_Paulo",
    page_load_strategy: str = "none",
    download_dir: str = "/home/selenium/Downloads",
    extension_path: Optional[str | Path] = None,
    use_safe_network_flags: bool = False,
    use_automation_flags: bool = False,
    accept_insecure_certs: bool = True,
) -> Options:
    """
        Função genérica para adicionar as configurações do selenoid
        Adicione em robôs novos para rodar o selenoid
    """

    # Opções básicas e necessárias
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", browser_version)

    if accept_insecure_certs:
        # Instrui o navegador a confiar implicitamente em certificados SSL inválidos, expirados ou autoassinados durante a sua sessão de testes
        options.set_capability("acceptInsecureCerts", True)

    # Opções
    # "normal" = espera a página carregar por completo
    # "eager"  = espera o DOMContentLoaded
    # "none"   = não espera carregar, serve para sites que demoram muito para carregar
    options.page_load_strategy = page_load_strategy

    # Configurações específicas do selenoid
    selenoid_options = {
        "enableVNC": enable_vnc,
        "enableLog": enable_log,
        "enableVideo": enable_video,
        "screenResolution": screen_resolution,
        "timeZone": timezone,
    }

    if log_name:
        selenoid_options["logName"] = log_name

    if video_name:
        selenoid_options["videoName"] = video_name

    if session_name:
        selenoid_options["name"] = session_name

    options.set_capability("selenoid:options", selenoid_options)

    # Flags do chrome que auxiliam no container
    options.add_argument("--window-size=1280,720")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-first-run")

    # Útil quando o chrome fica carregando infinitamente
    if use_safe_network_flags:
        options.add_argument("--disable-quic")
        options.add_argument("--disable-ipv6")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument(
            "--disable-features=UseDnsHttpsSvcb,UseDnsHttpsAlpn"
        )

    # Flags que auxiliam caso a automação esteja sendo detectada fácilmente
    if use_automation_flags:
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Preferências de download padrão
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True,
        "profile.default_content_settings.popups": 0,
    }

    options.add_experimental_option("prefs", prefs)

    # Extensão opcional passe caminho arquivo .crx
    if extension_path:
        extension_path = Path(extension_path).resolve()

        if not extension_path.exists():
            raise FileNotFoundError(f"Extension not found: {extension_path}")

        options.add_extension(str(extension_path))

    return options