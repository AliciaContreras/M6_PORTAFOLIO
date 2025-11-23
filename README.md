# 🧨 Laboratorio ACME - Gestión de Servicios

![ACME Corporation](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExejZ2eWh0a256enBqdTNoZ3U3eXNkaDNvZGN2aGc5eXpybWRpZzV6ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSxdQJIoiRXHl6/giphy.gif)

Plataforma web desarrollada en Django para la gestión operativa del famoso Laboratorio Acme (propiedad de Warner Bros.). Este sistema permite la administración de inventario de servicios excéntricos, gestión de personal y procesamiento de pedidos de clientes.

## 📋 Descripción del Proyecto

Este proyecto simula un entorno empresarial con roles jerárquicos y flujos de trabajo definidos, donde cada personaje de los Looney Tunes y Animaniacs tiene un papel específico:

*   **Administración:** Gestión total de usuarios y servicios (Admin: Steven Spielberg).
*   **Operaciones:** Jefes de laboratorio (Cerebro, etc.) que gestionan el catálogo de productos.
*   **Producción:** Trabajadores (Pinky, Yakko, etc.) que toman y finalizan los pedidos.
*   **Clientes:** Usuarios externos que se registran, solicitan servicios y monitorean el estado de sus pedidos.

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3, Django 5.
*   **Base de Datos:** SQLite (Modelo Relacional).
*   **Frontend:** HTML5, Jinja2 Templates, Bootstrap 5.
*   **Manejo de Archivos:** Pillow (para imágenes de perfil y servicios).

## 🚀 Funcionalidades Clave

1.  **Sistema de Roles (RBAC):**
    *   Permisos granulares utilizando el sistema `auth` nativo de Django.
    *   Vistas protegidas con `LoginRequiredMixin` y `UserPassesTestMixin`.
2.  **Gestión de Servicios:**
    *   CRUD completo (Crear, Leer, Actualizar, Eliminar) para los servicios, incluyendo imágenes.
3.  **Flujo de Pedidos:**
    *   **Cliente solicita** → Estado "Pendiente".
    *   **Trabajador toma pedido** → Estado "En Proceso".
    *   **Trabajador finaliza** → Estado "Terminado".
4.  **Panel de Usuario:**
    *   Cada usuario puede editar su perfil, incluyendo su foto y biografía.

## ⚙️ Instalación Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-DIRECTORIO>
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # Para Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar migraciones a la base de datos:**
    ```bash
    python manage.py migrate
    ```

5.  **Crear un superusuario (Opcional):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Cargar datos de prueba (Recomendado):**
    Para ver el proyecto con los personajes y servicios precargados, ejecuta:
    ```bash
    python manage.py loaddata datos_acme.json
    ```

7.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    ¡Ahora puedes acceder al proyecto en `http://127.0.0.1:8000`!

## 👤 Credenciales de Prueba (Demo)

Para acceder con los usuarios de prueba, utiliza la siguiente contraseña para todos: `root1234`

| Rol | Usuario |
| :--- | :--- |
| **Administrador** | `stevenspielberg` |
| **Jefes de Laboratorio** | `Cerebro`, `ProfesorRascahuele`, `Fenomenoide` |
| **Trabajadores** | `Pinky`, `HolaEnfermera`, `YakkoWarner`, `WakkoWarner`, `DotWarner` |
| **Cliente** | `Wile_coyote` |