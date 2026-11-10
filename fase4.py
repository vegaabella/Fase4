# Importa la librería para registrar eventos y errores en un archivo de texto (logs)
import logging

# Importa la librería estándar de Python para crear interfaces gráficas (ventanas, botones, etc.)
import tkinter as tk

# Importa clases para crear clases y métodos abstractos (herencia orientada a objetos)
from abc import ABC, abstractmethod

# Importa el módulo para manejar fechas y horas actuales (útil para las reservas)
from datetime import datetime

# Importa cuadros de diálogo emergentes (mensajes de éxito, error, advertencias) y widgets avanzados
from tkinter import messagebox, ttk

# ----------------------------------------------------------------------
# Configuración del Sistema de Logs (Guarda eventos y errores en archivo)
# ----------------------------------------------------------------------
# Configura el archivo 'app_errors.log' para registrar todo lo que pase en el sistema
logging.basicConfig(
    filename="app_errors.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# Escribe un mensaje inicial en el archivo de logs indicando que el programa arrancó
logging.info("=== Inicio del Sistema Software FJ ===")


# ----------------------------------------------------------------------
# Excepciones Personalizadas (Manejo robusto de errores)
# ----------------------------------------------------------------------
class SistemaFJError(Exception):
    """Excepción base para todas las fallas propias del sistema Software FJ."""

    pass


class ValidacionError(SistemaFJError):
    """Excepción para cuando los datos ingresados no son válidos o están incompletos."""

    pass


class ReservaError(SistemaFJError):
    """Excepción para errores de lógica de negocio (ej. intentar cerrar algo ya cerrado)."""

    pass


# ----------------------------------------------------------------------
# Arquitectura Orientada a Objetos (POO)
# ----------------------------------------------------------------------
class EntidadBase(ABC):
    """Clase abstracta base que obliga a tener un ID numérico en las entidades."""

    def _init_(self, id_entidad: int):
        self._id_entidad = id_entidad  # Guarda el identificador único interno

    @property
    def id_entidad(self):
        """Permite leer el ID de la entidad de forma segura."""
        return self._id_entidad


class Cliente(EntidadBase):
    """Clase que maneja los datos personales del cliente y su encapsulación."""

    def _init_(self, id_cliente: int, nombre: str = "", documento: str = ""):
        super()._init_(id_cliente)  # Hereda el ID de la clase base
        self.nombre = nombre  # Asigna el nombre usando el método 'setter'
        self.documento = documento  # Asigna el documento usando su 'setter'

    @property
    def nombre(self):
        """Retorna el nombre almacenado."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Valida que si el cliente no escribe nada, se guarde como 'Cliente Anónimo' (Cliente Opcional)."""
        self._nombre = valor.strip() if valor else "Cliente Anónimo"

    @property
    def documento(self):
        """Retorna el documento almacenado."""
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        """Valida el documento; si está vacío, coloca 'S/N' (Sin Número)."""
        self._documento = valor.strip() if valor else "S/N"

    def _str_(self):
        """Devuelve una representación en texto amigable del cliente."""
        return (
            f"{self._nombre} (Doc: {self._documento})"
            if self._nombre != "Cliente Anónimo"
            else "Cliente Anónimo"
        )


class Servicio(ABC):
    """Clase abstracta Servicio (Polimorfismo y Abstracción)."""

    def _init_(self, nombre_servicio: str, precio_base: float):
        self._nombre_servicio = nombre_servicio  # Nombre descriptivo del servicio
        self._precio_base = precio_base  # Costo base por unidad (hora, día, etc.)

    @property
    def nombre_servicio(self):
        """Devuelve el nombre del servicio."""
        return self._nombre_servicio

    @property
    def precio_base(self):
        """Devuelve el precio base."""
        return self._precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto obligatorio: cada servicio calculará su costo diferente."""
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Método abstracto obligatorio: describe los detalles específicos del servicio."""
        pass


class ReservaSala(Servicio):
    """Servicio 1: Hereda de Servicio para la reserva de salas."""

    def _init_(self, numero_sala: str, horas: int, tarifa_hora: float = 25000.0):
        super()._init_(
            "Reserva de Sala", tarifa_hora
        )  # Inicializa la clase padre
        if horas <= 0:
            raise ValidacionError(
                "Las horas de reserva deben ser mayores a 0."
            )  # Valida datos
        self.numero_sala = numero_sala  # Guarda la sala elegida
        self.horas = horas  # Guarda el número de horas

    def calcular_costo(self, descuento: float = 0.0) -> float:
        """Calcula el costo total multiplicando la tarifa por las horas (con opción de descuento)."""
        costo_total = self.precio_base * self.horas
        return costo_total * (1 - descuento)

    def obtener_descripcion(self) -> str:
        """Retorna los detalles particulares de la sala."""
        return f"Sala: {self.numero_sala} | Horas: {self.horas}"


class AlquilerEquipos(Servicio):
    """Servicio 2: Hereda de Servicio para el alquiler de equipos tecnológicos."""

    def _init_(
        self, tipo_equipo: str, cantidad: int, tarifa_diaria: float = 40000.0
    ):
        super()._init_("Alquiler de Equipos", tarifa_diaria)
        if cantidad <= 0:
            raise ValidacionError("La cantidad de equipos debe ser mayor a 0.")
        self.tipo_equipo = tipo_equipo
        self.cantidad = cantidad

    def calcular_costo(self, dias: int = 1, descuento: float = 0.0) -> float:
        """Calcula el costo total multiplicando tarifa, cantidad y días."""
        costo_total = self.precio_base * self.cantidad * dias
        return costo_total * (1 - descuento)

    def obtener_descripcion(self) -> str:
        """Retorna los detalles particulares del equipo."""
        return f"Equipo: {self.tipo_equipo} | Cantidad: {self.cantidad}"


class AsesoriaEspecializada(Servicio):
    """Servicio 3: Hereda de Servicio para asesorías profesionales."""

    def _init_(
        self, area: str, horas_asesoria: int, tarifa_hora: float = 60000.0
    ):
        super()._init_("Asesoría Especializada", tarifa_hora)
        if horas_asesoria <= 0:
            raise ValidacionError("Las horas de asesoría deben ser mayores a 0.")
        self.area = area
        self.horas_asesoria = horas_asesoria

    def calcular_costo(self, incluye_informe: bool = False) -> float:
        """Calcula el costo por horas con un posible recargo por informe opcional."""
        costo_total = self.precio_base * self.horas_asesoria
        if incluye_informe:
            costo_total += 20000.0
        return costo_total

    def obtener_descripcion(self) -> str:
        """Retorna los detalles de la asesoría."""
        return f"Área: {self.area} | Horas: {self.horas_asesoria}"


class Reserva(EntidadBase):
    """Clase que une al Cliente, el Servicio, la fecha y el estado de la reserva."""

    def _init_(
        self, id_reserva: int, servicio: Servicio, cliente: Cliente = None
    ):
        super()._init_(id_reserva)
        self.servicio = servicio  # Asocia el objeto servicio
        self.cliente = (
            cliente if cliente else Cliente(0)
        )  # Asocia el cliente (o anónimo si no hay)
        self.fecha_creacion = datetime.now()  # Guarda la fecha y hora exacta
        self.estado = "Activa"  # Estado inicial de la reserva
        self.costo_total = (
            self.servicio.calcular_costo()
        )  # Calcula el costo automático

    def cerrar_reserva(self):
        """Cambia el estado de la reserva a 'Cerrada' de forma permanente en memoria."""
        if self.estado == "Cerrada":
            raise ReservaError("La reserva ya se encuentra cerrada.")
        self.estado = "Cerrada"


# ----------------------------------------------------------------------
# Interfaz Gráfica Tkinter
# ----------------------------------------------------------------------
class AplicacionSoftwareFJ:
    """Clase principal que construye y controla la ventana gráfica."""

    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema Integral de Gestión")  # Título
        self.root.geometry("850x650")  # Tamaño de la ventana
        self.root.configure(bg="#f4f6f9")  # Color de fondo general

        self.lista_reservas = (
            []
        )  # Memoria temporal: lista donde se guardan los objetos creados
        self.contador_id = 1  # Autoincrementable para el ID de cada reserva

        self._crear_interfaz()  # Llama al método que dibuja los elementos visuales

    def _crear_interfaz(self):
        """Construye todos los botones, campos y tablas de la ventana."""
        # Franja superior para el nombre de la empresa
        frame_header = tk.Frame(self.root, bg="#1e293b",)
        frame_header.pack(fill=tk.X, pady=15)

        # Etiqueta con el nombre requerido: SOFTWARE FJ
        lbl_titulo = tk.Label(
            frame_header,
            text="SOFTWARE FJ",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#1e293b",
        )
        lbl_titulo.pack()

        lbl_subtitulo = tk.Label(
            frame_header,
            text="Sistema Integral de Gestión de Servicios y Reservas",
            font=("Helvetica", 10),
            fg="#cbd5e1",
            bg="#1e293b",
        )
        lbl_subtitulo.pack()

        # Contenedor principal de la interfaz
        main_frame = tk.Frame(self.root, bg="#f4f6f9", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cuadro de formulario para registrar datos
        lbl_frame_form = tk.LabelFrame(
            main_frame,
            text=" Registrar Nueva Reserva ",
            font=("Helvetica", 11, "bold"),
            bg="white",
            padx=15,
            pady=15,
        )
        lbl_frame_form.pack(fill=tk.X, pady=(0, 15))

        # Campo opcional: Nombre del cliente
        tk.Label(
            lbl_frame_form,
            text="Nombre Cliente (Opcional):",
            bg="white",
            font=("Helvetica", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_cliente_nombre = tk.Entry(lbl_frame_form, width=30)
        self.entry_cliente_nombre.grid(row=0, column=1, padx=10, pady=5)

        # Campo opcional: Documento del cliente
        tk.Label(
            lbl_frame_form,
            text="Documento (Opcional):",
            bg="white",
            font=("Helvetica", 9, "bold"),
        ).grid(row=0, column=2, sticky="w", pady=5)
        self.entry_cliente_doc = tk.Entry(lbl_frame_form, width=20)
        self.entry_cliente_doc.grid(row=0, column=3, padx=10, pady=5)

        # Menú desplegable para elegir el tipo de servicio
        tk.Label(
            lbl_frame_form,
            text="Tipo de Servicio:",
            bg="white",
            font=("Helvetica", 9, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=5)
        self.combo_servicio = ttk.Combobox(
            lbl_frame_form,
            values=[
                "Reserva de Sala",
                "Alquiler de Equipos",
                "Asesoría Especializada",
            ],
            state="readonly",
            width=27,
        )
        self.combo_servicio.current(0)  # Selecciona el primero por defecto
        self.combo_servicio.grid(row=1, column=1, padx=10, pady=5)
        self.combo_servicio.bind(
            "<<ComboboxSelected>>", self._actualizar_campos
        )  # Evento al cambiar selección

        # Etiquetas y cuadros dinámicos para los detalles del servicio 1
        self.lbl_detalle_1 = tk.Label(
            lbl_frame_form,
            text="Nº de Sala:",
            bg="white",
            font=("Helvetica", 9, "bold"),
        )
        self.lbl_detalle_1.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_detalle_1 = tk.Entry(lbl_frame_form, width=30)
        self.entry_detalle_1.grid(row=2, column=1, padx=10, pady=5)
        self.entry_detalle_1.insert(0, "Sala A-101")

        # Etiquetas y cuadros dinámicos para los detalles del servicio 2
        self.lbl_detalle_2 = tk.Label(
            lbl_frame_form,
            text="Horas:",
            bg="white",
            font=("Helvetica", 9, "bold"),
        )
        self.lbl_detalle_2.grid(row=2, column=2, sticky="w", pady=5)
        self.entry_detalle_2 = tk.Entry(lbl_frame_form, width=20)
        self.entry_detalle_2.grid(row=2, column=3, padx=10, pady=5)
        self.entry_detalle_2.insert(0, "2")

        # Botón para guardar el registro en memoria
        btn_guardar = tk.Button(
            lbl_frame_form,
            text="Guardar y Activar Reserva",
            command=self._guardar_reserva,
            bg="#2563eb",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
        )
        btn_guardar.grid(row=3, column=0, columnspan=4, pady=10)

        # Sección de la tabla visual (Treeview) para mostrar las reservas guardadas
        lbl_frame_tabla = tk.LabelFrame(
            main_frame,
            text=" Reservas y Servicios Activos (Persistencia en Memoria) ",
            font=("Helvetica", 11, "bold"),
            bg="white",
            padx=10,
            pady=10,
        )
        lbl_frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = (
            "ID",
            "Cliente",
            "Servicio",
            "Detalles",
            "Costo Total",
            "Estado",
        )
        self.tree = ttk.Treeview(
            lbl_frame_tabla, columns=columnas, show="headings"
        )

        # Define los encabezados de las columnas de la tabla
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Servicio", text="Servicio")
        self.tree.heading("Detalles", text="Detalles del Servicio")
        self.tree.heading("Costo Total", text="Costo ($)")
        self.tree.heading("Estado", text="Estado")

        # Ajusta los anchos de las columnas en pantalla
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Cliente", width=160)
        self.tree.column("Servicio", width=150)
        self.tree.column("Detalles", width=220)
        self.tree.column("Costo Total", width=90, anchor="e")
        self.tree.column("Estado", width=80, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(
            lbl_frame_tabla, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botón para cerrar/finalizar la reserva seleccionada
        btn_cerrar = tk.Button(
            main_frame,
            text="Cerrar/Finalizar Reserva Seleccionada",
            command=self._cerrar_reserva,
            bg="#dc2626",
            fg="white",
            font=("Helvetica", 9, "bold"),
            relief="flat",
            pady=5,
        )
        btn_cerrar.pack(fill=tk.X, pady=(10, 0))

    def _actualizar_campos(self, event=None):
        """Cambia los textos de los campos de acuerdo al servicio que el usuario elija."""
        servicio = self.combo_servicio.get()
        self.entry_detalle_1.delete(0, tk.END)
        self.entry_detalle_2.delete(0, tk.END)

        if servicio == "Reserva de Sala":
            self.lbl_detalle_1.config(text="Nº de Sala:")
            self.lbl_detalle_2.config(text="Horas:")
            self.entry_detalle_1.insert(0, "Sala A-101")
            self.entry_detalle_2.insert(0, "2")
        elif servicio == "Alquiler de Equipos":
            self.lbl_detalle_1.config(text="Tipo de Equipo:")
            self.lbl_detalle_2.config(text="Cantidad:")
            self.entry_detalle_1.insert(0, "Portátil Core i7")
            self.entry_detalle_2.insert(0, "1")
        elif servicio == "Asesoría Especializada":
            self.lbl_detalle_1.config(text="Área Asesoría:")
            self.lbl_detalle_2.config(text="Horas:")
            self.entry_detalle_1.insert(0, "Arquitectura de Software")
            self.entry_detalle_2.insert(0, "3")

    def _guardar_reserva(self):
        """Bloque Try/Except para capturar errores, crear objetos y guardarlos permanentemente en memoria."""
        try:
            nombre_cliente = self.entry_cliente_nombre.get()
            doc_cliente = self.entry_cliente_doc.get()
            # Si los campos del cliente están vacíos, se crea como None (Cliente Opcional)
            cliente_obj = (
                Cliente(self.contador_id, nombre_cliente, doc_cliente)
                if nombre_cliente or doc_cliente
                else None
            )

            tipo_servicio = self.combo_servicio.get()
            val1 = self.entry_detalle_1.get()
            val2 = self.entry_detalle_2.get()

            if not val1 or not val2:
                raise ValidacionError(
                    "Todos los campos del servicio son obligatorios."
                )

            # Instanciación polimórfica según la selección del usuario
            if tipo_servicio == "Reserva de Sala":
                if not val2.isdigit():
                    raise ValidacionError("Las horas deben ser un número entero.")
                servicio_obj = ReservaSala(
                    numero_sala=val1, horas=int(val2)
                )

            elif tipo_servicio == "Alquiler de Equipos":
                if not val2.isdigit():
                    raise ValidacionError(
                        "La cantidad debe ser un número entero."
                    )
                servicio_obj = AlquilerEquipos(
                    tipo_equipo=val1, cantidad=int(val2)
                )

            elif tipo_servicio == "Asesoría Especializada":
                if not val2.isdigit():
                    raise ValidacionError("Las horas deben ser un número entero.")
                servicio_obj = AsesoriaEspecializada(
                    area=val1, horas_asesoria=int(val2)
                )

            # Crea el objeto reserva principal y lo añade a la lista en memoria RAM
            reserva = Reserva(self.contador_id, servicio_obj, cliente_obj)
            self.lista_reservas.append(reserva)
            self.contador_id += 1

            logging.info(
                f"Reserva #{reserva.id_entidad} guardada con éxito para: {reserva.cliente}"
            )
            self._refrescar_tabla()  # Actualiza la tabla visual
            messagebox.showinfo(
                "Éxito",
                f"Reserva #{reserva.id_entidad} registrada y guardada exitosamente.",
            )

        except (ValidacionError, ReservaError) as e:
            logging.warning(
                f"Error de validación/negocio al guardar reserva: {e}"
            )
            messagebox.showerror("Error de Datos", str(e))
        except Exception as e:
            logging.error(f"Error inesperado del sistema: {e}", exc_info=True)
            messagebox.showerror("Error Crítico", f"Ocurrió un error: {e}")

    def _refrescar_tabla(self):
        """Limpia la tabla visual y vuelve a cargar todos los objetos de la lista en memoria."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for res in self.lista_reservas:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    res.id_entidad,
                    str(res.cliente),
                    res.servicio.nombre_servicio,
                    res.servicio.obtener_descripcion(),
                    f"${res.costo_total:,.2f}",
                    res.estado,
                ),
            )

    def _cerrar_reserva(self):
        """Busca la reserva seleccionada en la tabla y la marca como cerrada."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Por favor seleccione una reserva de la lista."
            )
            return

        item = self.tree.item(seleccion)
        reserva_id = item["values"][0]

        try:
            # Busca el objeto en la lista usando su ID
            reserva = next(
                (r for r in self.lista_reservas if r.id_entidad == reserva_id),
                None,
            )
            if reserva:
                reserva.cerrar_reserva()  # Ejecuta el cierre del servicio
                logging.info(f"Reserva #{reserva_id} fue cerrada.")
                self._refrescar_tabla()
                messagebox.showinfo(
                    "Reserva Cerrada",
                    f"La reserva #{reserva_id} ha sido finalizada correctamente.",
                )
        except ReservaError as e:
            logging.warning(f"Error al cerrar la reserva #{reserva_id}: {e}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            logging.error(f"Error inesperado al cerrar reserva: {e}")
            messagebox.showerror("Error", f"No se pudo cerrar la reserva: {e}")


# ----------------------------------------------------------------------
# Punto de entrada de la aplicación
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("Iniciando aplicacion")
    root = tk.Tk()  # Crea la ventana raíz de Tkinter
    print("ventana raiz")
    app = AplicacionSoftwareFJ(root)  # Instancia la clase principal de la aplicación
    root.mainloop()
    print("aplicacion cerrada")
