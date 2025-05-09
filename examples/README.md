# Ejemplos de Código

## Juego de Snake en Python

Este directorio contiene un juego de Snake implementado en Python siguiendo principios de código limpio y programación orientada a objetos.

### Requisitos

Para ejecutar el juego, necesitarás:

- Python 3.6 o superior
- Pygame (biblioteca para desarrollo de juegos)

### Instalación

```bash
# Instalar Pygame
pip install pygame
```

### Ejecución

```bash
# Navegar al directorio de ejemplos
cd examples

# Ejecutar el juego
python snake_game.py
```

### Controles

- Flechas direccionales: Controlar la dirección de la serpiente
- ESC: Salir del juego
- R: Reiniciar el juego después de perder

### Características del Código

El código implementa los siguientes principios de código limpio:

1. **Responsabilidad Única**: Cada clase tiene una única responsabilidad (Snake, Food, Game, etc.)
2. **Encapsulamiento**: Los datos y comportamientos relacionados están agrupados en clases
3. **Nombres Descriptivos**: Variables y funciones con nombres claros que indican su propósito
4. **Comentarios Útiles**: Documentación de clases y métodos para explicar su funcionamiento
5. **Tipado**: Uso de type hints para mejorar la legibilidad y mantenibilidad

### Estructura del Código

- `Direction`: Enumeración para las direcciones de movimiento
- `Color`: Clase para definir colores utilizados en el juego
- `Config`: Configuración global del juego
- `Position`: Clase para manejar posiciones en la cuadrícula
- `Food`: Representa la comida que la serpiente debe comer
- `Snake`: Implementa la lógica de la serpiente controlada por el jugador
- `Game`: Clase principal que coordina todos los elementos del juego
