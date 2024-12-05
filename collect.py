
''' 60 follows por hora // 150 follows por dia

200 unfollows por hora // 4000 unfollows por dia '''


'''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configura tus credenciales y la cuenta objetivo
USERNAME = 'membranas_moron'
PASSWORD = 'membrana moron'
TARGET_ACCOUNT = 'membranasferrari'  # La cuenta cuyos seguidores quieres obtener
FOLLOWERS_LIMIT = 1000  # Límite de seguidores a extraer

# Inicializa el navegador
driver = webdriver.Chrome()

try:
    # Cargar usuarios existentes desde el archivo (si existe)
    existing_followers = set()
    try:
        with open("followers_list(3).txt", "r") as file:
            existing_followers = set(line.strip() for line in file)
    except FileNotFoundError:
        print("No se encontró el archivo, se creará uno nuevo.")

    # Abre Instagram
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Inicia sesión
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "password").send_keys('\n')
    time.sleep(5)

    # Omitir ventanas emergentes
    try:
        driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
        time.sleep(2)
    except:
        pass

    # Navega a la cuenta objetivo
    driver.get(f"https://www.instagram.com/{TARGET_ACCOUNT}/")
    time.sleep(3)

    # Haz clic en la sección de seguidores
    followers_link = driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]")
    followers_link.click()
    time.sleep(3)

    # Espera hasta que el modal de seguidores sea visible
    followers_popup = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']"))
    )

    # Extrae los seguidores
    followers_list = []

    # Desplázate por la lista para cargar más usuarios
    for _ in range(int(FOLLOWERS_LIMIT / 10)):  # Ajusta el rango según el límite
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
        time.sleep(2)

    # Obtén los nombres de usuario visibles
    followers = followers_popup.find_elements(By.XPATH, "//a[contains(@href, '/')]")
    for follower in followers:
        username = follower.get_attribute("href").split("/")[-2]
        # Filtra los enlaces no relacionados con usuarios
        if username.isalnum() and len(username) > 1 and not username.startswith(('explore', 'help', 'about', 'privacy', 'terms', 'locations', 'lite', 'blog', 'inbox', 'meta', 'instagram')): 
            followers_list.append(username)
        if len(followers_list) >= FOLLOWERS_LIMIT:
            break

    # Combina las listas, eliminando duplicados
    new_followers = set(followers_list) - existing_followers

    # Guarda los nombres de usuario únicos (existentes + nuevos) en un archivo .txt
    with open("followers_list(3).txt", "a") as file:
        for user in new_followers:
            file.write(f"{user}\n")

    print(f"Nuevos usuarios agregados al archivo:")
    print(new_followers)

finally:
    # Cierra el navegador
    driver.quit()'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configura tus credenciales
USERNAME = 'membranas_moron'
PASSWORD = 'membrana moron'

# Lee la lista de seguidores desde el archivo txt
with open('followers_list(3).txt', 'r') as file:
    followers_list = file.readlines()

# Elimina saltos de línea y espacios extras de cada nombre
followers_list = [follower.strip() for follower in followers_list]

# Inicializa el navegador
driver = webdriver.Chrome()

try:
    # Abre Instagram
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Inicia sesión
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(5)

    # Omitir ventanas emergentes
    try:
        driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
        time.sleep(2)
    except:
        pass

    # Recorre la lista de seguidores y los sigue
    follow_count = 0  # Contador de personas seguidas
    max_follows = 60  # Máximo de personas a seguir

    for user in followers_list:
        if follow_count >= max_follows:
            print("Se alcanzó el límite de 60 personas seguidas. Finalizando el programa.")
            break

        try:
            # Navegar al perfil del usuario
            driver.get(f"https://www.instagram.com/{user}/")
            time.sleep(3)

            # Hacer clic en el botón de seguir (usando el nuevo XPath)
            follow_button = driver.find_element(By.XPATH, "//button[contains(@class, '_acan') and contains(@class, '_acap')]")
            if follow_button:
                follow_button.click()
                follow_count += 1
                print(f"Siguiendo a {user} ({follow_count}/{max_follows})")
                time.sleep(2)  # Esperar para no hacer las peticiones demasiado rápido
            else:
                print(f"Ya sigues a {user} o no se puede seguir.")
        except Exception as e:
            print(f"No se pudo seguir a {user}: {str(e)}")

finally:
    # Cierra el navegador
    driver.quit()

