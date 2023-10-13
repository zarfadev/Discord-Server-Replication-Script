from os import system
import psutil
import os
from pypresence import Presence
import time
import sys
import discord
import json
import traceback
from rich.table import Table
from rich.console import Console
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.progress import Progress
import asyncio
from colorama import Fore, init, Style
import platform
import inquirer
from cloner import Clone

version = '1.4'
#clones = {'Clones_test_done': 0}
console = Console()


def loading(seconds):
    with Progress() as progress:
        task = progress.add_task("", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)


def clearall():
    system('clear')
    print(f"""{Style.BRIGHT}{Fore.RED}
@@@@@@@@   @@@@@@   @@@@@@@   @@@@@@@@   @@@@@@   @@@        @@@@@@      @@@  @@@     @@@@@@@@@@    @@@@@@   @@@  @@@  @@@  @@@  @@@  @@@  @@@  @@@  
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@       @@@@@@@@     @@@  @@@     @@@@@@@@@@@  @@@@@@@@  @@@  @@@  @@@  @@@  @@@  @@@  @@@  @@@  
     @@!  @@!  @@@  @@!  @@@  @@!       @@!  @@@  @@!       @@!  @@@     @@!  !@@     @@! @@! @@!  @@!  @@@  @@!  !@@  @@!  @@@  @@!  !@@  @@!  @@@  
    !@!   !@!  @!@  !@!  @!@  !@!       !@!  @!@  !@!       !@!  @!@     !@!  @!!     !@! !@! !@!  !@!  @!@  !@!  @!!  !@!  @!@  !@!  @!!  !@!  @!@  
   @!!    @!@!@!@!  @!@!!@!   @!!!:!    @!@!@!@!  @!!       @!@!@!@!      !@@!@!      @!! !!@ @!@  @!@!@!@!  @!@@!@!   @!@  !@!  @!@@!@!   @!@  !@!  
  !!!     !!!@!!!!  !!@!@!    !!!!!:    !!!@!!!!  !!!       !!!@!!!!       @!!!       !@!   ! !@!  !!!@!!!!  !!@!!!    !@!  !!!  !!@!!!    !@!  !!!  
 !!:      !!:  !!!  !!: :!!   !!:       !!:  !!!  !!:       !!:  !!!      !: :!!      !!:     !!:  !!:  !!!  !!: :!!   !!:  !!!  !!: :!!   !!:  !!!  
:!:       :!:  !:!  :!:  !:!  :!:       :!:  !:!   :!:      :!:  !:!     :!:  !:!     :!:     :!:  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  
 :: ::::  ::   :::  ::   :::   ::       ::   :::   :: ::::  ::   :::      ::  :::     :::     ::   ::   :::   ::  :::  ::::: ::   ::  :::  ::::: ::  
: :: : :   :   : :   :   : :   :         :   : :  : :: : :   :   : :      :   ::       :      :     :   : :   :   :::   : :  :    :   :::   : :  :   
{Style.RESET_ALL}{Fore.RESET}""")
    print(
        f"{Style.BRIGHT}{Fore.GREEN}Nuevo clonador en proceso de creación, para más información visite: {Fore.BLUE}https://discord.gg/panelextortion{Style.RESET_ALL}{Fore.RESET}"
    )


def get_user_preferences():
    preferences = {}
    preferences['guild_edit'] = True
    preferences['channels_delete'] = True
    preferences['roles_create'] = True
    preferences['categories_create'] = True
    preferences['channels_create'] = True
    preferences['emojis_create'] = False

    def map_boolean_to_string(value):
        return "Si" if value else "No"

    panel_title = "Config BETA"
    panel_content = "\n"
    panel_content += f"- Cambia el nombre y el icono del servidor: {map_boolean_to_string(preferences.get('guild_edit', False))}\n"
    panel_content += f"- Borrar canales del servidor de destino: {map_boolean_to_string(preferences.get('channels_delete', False))}\n"
    panel_content += f"- Clonar Roles: {map_boolean_to_string(preferences.get('roles_create', False))}\n"
    panel_content += f"- Clonar Categorías: {map_boolean_to_string(preferences.get('categories_create', False))}\n"
    panel_content += f"- Clonar Canales: {map_boolean_to_string(preferences.get('channels_create', False))}\n"
    panel_content += f"- Clonar Emojis: {map_boolean_to_string(preferences.get('emojis_create', False))}\n"
    console.print(
        RichPanel(panel_content,
                  title=panel_title,
                  style="bold blue",
                  width=70))

    questions = [
        inquirer.List('reconfigure',
                      message='¿Desea reconfigurar los ajustes por defecto?',
                      choices=['Si', 'No'],
                      default='No')
    ]

    answers = inquirer.prompt(questions)

    reconfigure = answers['reconfigure']
    if reconfigure == 'Si':
        questions = [
            inquirer.Confirm(
                'guild_edit',
                message='¿Quieres editar el icono y el nombre del servidor?',
                default=False),
            inquirer.Confirm('channels_delete',
                             message='¿Quieres borrar los canales?',
                             default=False),
            inquirer.Confirm(
                'roles_create',
                message='¿Desea clonar roles? (NO SE RECOMIENDA DESACTIVAR)',
                default=False),
            inquirer.Confirm('categories_create',
                             message='¿Quiere clonar categorías?',
                             default=False),
            inquirer.Confirm('channels_create',
                             message='¿Quieres clonar canales?',
                             default=False),
            inquirer.Confirm(
                'emojis_create',
                message=
                '¿Quieres clonar emojis? (SE RECOMIENDA HABILITAR ESTA CLONACIÓN EN SOLO PARA EVITAR ERRORES)',
                default=False)
        ]

        answers = inquirer.prompt(questions)
        preferences['guild_edit'] = answers['guild_edit']
        preferences['channels_delete'] = answers['channels_delete']
        preferences['roles_create'] = answers['roles_create']
        preferences['categories_create'] = answers['categories_create']
        preferences['channels_create'] = answers['channels_create']
        preferences['emojis_create'] = answers['emojis_create']

    clearall()
    return preferences


versao_python = sys.version.split()[0]


def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)


client = discord.Client()
if platform.system() == "Windows":
    system("cls")
else:
    print(chr(27) + "[2J")
    clearall()

while True:
    token = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Introduzca su token para continuar:{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild_s = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Introduzca el ID del servidor que desea replicar:{Style.RESET_ALL}{Fore.RESET}\n >'
    )
    guild = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}Introduzca el ID del servidor de destino para pegar el servidor copiado:{Style.RESET_ALL}{Fore.RESET}\n>'
    )
    clearall()
    print(f'{Style.BRIGHT}{Fore.GREEN}Los valores insertados son:')
    token_length = len(token)
    hidden_token = "*" * token_length
    print(
        f'{Style.BRIGHT}{Fore.GREEN}Su token: {Fore.YELLOW}{hidden_token}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID del servidor a replicar: {Fore.YELLOW}{guild_s}{Style.RESET_ALL}{Fore.RESET}'
    )
    print(
        f'{Style.BRIGHT}{Fore.GREEN}ID del servidor de destino para pegar el servidor copiado: {Fore.YELLOW}{guild}{Style.RESET_ALL}{Fore.RESET}'
    )
    confirm = input(
        f'{Style.BRIGHT}{Fore.MAGENTA}¿Son correctos los valores? {Fore.YELLOW}(Y/N){Style.RESET_ALL}{Fore.RESET}\n >'
    )
    if confirm.upper() == 'Y':
        if not guild_s.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}El ID del servidor a replicar debe contener sólo números.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not guild.isnumeric():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}El ID del servidor de destino sólo debe contener números.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if not token.strip() or not guild_s.strip() or not guild.strip():
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}Uno o más campos están en blanco.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        if len(token.strip()) < 3 or len(guild_s.strip()) < 3 or len(
                guild.strip()) < 3:
            clearall()
            print(
                f'{Style.BRIGHT}{Fore.RED}Uno o más campos tienen menos de 3 caracteres.{Style.RESET_ALL}{Fore.RESET}'
            )
            continue
        break
    elif confirm.upper() == 'N':
        clearall()
    else:
        clearall()
        print(
            f'{Style.BRIGHT}{Fore.RED}Opción no válida. Por favor, introduzca Y o N.{Style.RESET_ALL}{Fore.RESET}'
        )
input_guild_id = guild_s
output_guild_id = guild
token = token
clearall()


@client.event
async def on_ready():
    try:
        start_time = time.time()
        global clones
        table = Table(title="Versions", style="bold magenta", width=85)
        table.add_column("Component", width=35)
        table.add_column("Version", style="cyan", width=35)
        table.add_row("Cloner", version)
        table.add_row("Discord.py", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(RichPanel(table))
        console.print(
            RichPanel(f" Autenticación correcta como {client.user.name}",
                      style="bold green",
                      width=69))
        print(f"\n")
        loading(5)
        clearall()
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        preferences = get_user_preferences()

        if not any(preferences.values()):
            preferences = {k: True for k in preferences}

        if preferences['guild_edit']:
            await Clone.guild_edit(guild_to, guild_from)
        if preferences['channels_delete']:
            await Clone.channels_delete(guild_to)
        if preferences['roles_create']:
            await Clone.roles_create(guild_to, guild_from)
        if preferences['categories_create']:
            await Clone.categories_create(guild_to, guild_from)
        if preferences['channels_create']:
            await Clone.channels_create(guild_to, guild_from)
        if preferences['emojis_create']:
            await Clone.emojis_create(guild_to, guild_from)

        end_time = time.time()
        duration = end_time - start_time
        duration_str = time.strftime("%M:%S", time.gmtime(duration))
        print("\n\n")
        print(
            f"{Style.BRIGHT}{Fore.BLUE}El servidor se ha clonado correctamente en {Fore.YELLOW}{duration_str}{Style.RESET_ALL}"
        )
        print(
            f"{Style.BRIGHT}{Fore.BLUE}Visita nuestro servidor Discord: {Fore.YELLOW}https://discord.gg/panelextortion{Style.RESET_ALL}"
        )
        #with open('saves.json', 'r') as f:
        #  clones = json.load(f)
        #clones['Clones_test_done'] += 1
        # with open('saves.json', 'w') as f:
        #  json.dump(clones, f)
        print(
            f"{Style.BRIGHT}{Fore.BLUE}Finalización del proceso y cierre de sesión en {Fore.YELLOW}{client.user}"
        )
        await asyncio.sleep(30)
        await client.close()

    except discord.LoginFailure:
        print(
            "No se ha podido autenticar con la cuenta. Compruebe si el token es correcto."
        )
    except discord.Forbidden:
        print("La clonación falló debido a permisos insuficientes.")
    except discord.NotFound:
        print(
            "No se ha podido encontrar uno de los elementos a copiar (canales, categorías, etc.)."
        )
    except discord.HTTPException:
        print(
            "Se ha producido un error de comunicación con la API de Discord. El código continuará desde donde lo dejó en 20 segundos."
        )
        loading(20)
        await Clone.emojis_create(guild_to, guild_from)
    except asyncio.TimeoutError:
        print("Se ha producido un error: TimeOut")
    except Exception as e:
        print(Fore.RED + "Se ha producido un error:", e)
        print("\n")
        traceback.print_exc()
        panel_text = (
            f"1. ID de servidor incorrecto\n"
            f"2. Usted no está en el servidor insertado\n"
            f"3. El servidor insertado no existe\n"
            f"¿Aún no se ha resuelto? Póngase en contacto con el desarrollador en [link=https://discord.gg/panelextortion]https://discord.gg/panelextortion[/link]"
        )
        console.print(
            RichPanel(panel_text,
                      title="Posibles causas y soluciones",
                      style="bold red",
                      width=70))
        print(
            Fore.YELLOW +
            "\nEl código se reiniciará en 20 segundos. Si no quieres esperar, actualiza la página y vuelve a empezar."
        )
        print(Style.RESET_ALL)
        loading(20)
        restart()
        print(Fore.RED + "Reiniciando...")


try:
    client.run(token, bot=False)
except discord.LoginFailure:
    print(Fore.RED + "El token insertado no es válido")
    print(
        Fore.YELLOW +
        "\n\nEl código se reiniciará en 10 segundos. Si no quieres esperar, actualiza la página y vuelve a empezar."
    )
    print(Style.RESET_ALL)
    loading(10)
    restart()
    clearall()
    print(Fore.RED + "Reiniciando...")
