#======================================================================================
#======================================================================================
import pandas as pd
import streamlit as st
#Autorización Google spreadsheets (API)
from google.oauth2.service_account import Credentials
from gspread_pandas import Spread, Client
from ast import literal_eval
#Manejo de fechas
from datetime import datetime
#Logo en página
from PIL import Image
import urllib.request
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#Listas para utilizas en el documento
#Empresa/Hub
e_hub = sorted(["EasyGo","Lets Advertise","Administración","RRHH","TPP","TPP Extreme","TPP Fénix","TPP ULTRA","TOM"])
#--------------------------------------------------------------------------------------
#Puestos registrados
nombre_puesto = sorted(['Gerente Contable y Auditor Regional','Asistente Contable','Intendencia y Mensajería','Jefe Local de Contabilidad','Programador/a','Encargado del Dpto. de IT ','Asistente de IT', 'Project Manager','Front-End Developer','Asesor Comercial','Gerente de Desarrollo, Easy Go','Diseñador/a Gráfico/a','Asistente Lets Advertise','SEO','Gerente de Medios','Científico de Datos','Gerente de Recursos Humanos','Asistente de Recursos Humanos','Asistente TOM','Social Media Manager','Ejecutiva de Cuentas','Asistente de Cuentas','Gerente de División TOM','Trafficker','Gerente de Ventas','Gerente de División TPP','Gerente de Operaciones','Gerente Financiero Administrativo','Gerente Comercial','Gerente de Nuevos Negocios','Copywritter'])
#--------------------------------------------------------------------------------------
#Nombres de las columnas nuevo documento
name_columns = ["Nombres", "Apellidos", "Género", "Fecha de Nacimiento","CUI","Empresa/Hub", "Email", "Puesto", "Lugar Diversificado", "Nombre Diversificado", "Estado Diversificado", "Lugar Licenciatura", "Nombre Licenciatura", "Estado Licenciatura", "Semestre", "Lugar Maestría/Posgrado", "Nombre Maestría/Posgrado", "Estado Maestría/Posgrado", "Lugar Cursos/Diplomados/Certificaciones", "Nombre Cursos/Diplomados/Certificaciones", "Estado Cursos/Diplomados/Certificaciones"]
#--------------------------------------------------------------------------------------
#Configuración de la página para que esta sea ancha
#Configuración para logo en la página
URL = 'https://i.imgur.com/PDSH54d.png'
img = Image.open(urllib.request.urlopen(URL))
st.set_page_config(page_title='Formulario Actualización', page_icon = img, layout="wide")
#--------------------------------------------------------------------------------------
#Configuración para ocultar menu de hamburguesa y pie de página
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html = True)
#======================================================================================
#======================================================================================
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_info(st.secrets["s_g"], scopes=scope)
client = Client(scope=scope, creds=credentials)
if 'spread' not in st.session_state:
    st.session_state.spread = Spread("Output_Form", client=client)

df = st.session_state.spread.sheet_to_df().reset_index()
#======================================================================================
#======================================================================================
#Session state
    #DataFrames
if 'df_filtro' not in st.session_state:
    st.session_state.df_filtro = pd.DataFrame(columns = name_columns)
if 'df_general' not in st.session_state:
    st.session_state.df_general = pd.DataFrame(columns = name_columns)
    #======================================================================================
    #Listas
    #'lugar_d', 'lugar_l', 'lugar_m', 'lugar_c'
if 'lugar_d' not in st.session_state:
    st.session_state.lugar_d = []
if 'lugar_l' not in st.session_state:
    st.session_state.lugar_l = []
if 'lugar_m' not in st.session_state:
    st.session_state.lugar_m = []
if 'lugar_c' not in st.session_state:
    st.session_state.lugar_c = []
    #'titulo_d', 'titulo_l', 'titulo_m', 'titulo_c'
if 'titulo_d' not in st.session_state:
    st.session_state.titulo_d = []
if 'titulo_l' not in st.session_state:
    st.session_state.titulo_l = []
if 'titulo_m' not in st.session_state:
    st.session_state.titulo_m = []
if 'titulo_c' not in st.session_state:
    st.session_state.titulo_c = []
    #'e_d', 'e_l', 'e_m', 'e_c', 'e_ll'
if 'e_d' not in st.session_state:
    st.session_state.e_d = []
if 'e_l' not in st.session_state:
    st.session_state.e_l = []
if 'e_m' not in st.session_state:
    st.session_state.e_m = []
if 'e_c' not in st.session_state:
    st.session_state.e_c = []
if 'e_ll' not in st.session_state:
    st.session_state.e_ll = []
    #count_ab - Diversificado, count_al - Licenciatura, count_am - Maestría, count_acc - Diplomados/Cursos/Certificados
if 'count_ac' not in st.session_state:
    st.session_state.count_ac = 0
if 'count_al' not in st.session_state:
    st.session_state.count_al = 0
if 'count_am' not in st.session_state:
    st.session_state.count_am = 0
if 'count_acc' not in st.session_state:
    st.session_state.count_acc = 0
    #count_pi_ac - Diversificado
if 'count_pi_ac' not in st.session_state:
    st.session_state.count_pi_ac = 1
if 'count_pi_al' not in st.session_state:
    st.session_state.count_pi_al = 1
if 'count_pi_am' not in st.session_state:
    st.session_state.count_pi_am = 1
if 'count_pi_acc' not in st.session_state:
    st.session_state.count_pi_acc = 1
#Información general
if 'count_pi_ag' not in st.session_state:
    st.session_state.count_pi_ag = 1
    #Nuevo
if 'n_b_d' not in st.session_state:
    st.session_state.n_b_d = False
    #Explorar
if 'explorar' not in st.session_state:
    st.session_state.explorar = ""
    #Estado anterior explorar
if 'p_explorar' not in st.session_state:
    st.session_state.p_explorar = ""
    
if 'nombres_f' not in st.session_state:
    st.session_state.nombres_f = ""
if 'apellidos_f' not in st.session_state:
    st.session_state.apellidos_f = ""
if 'genero_f' not in st.session_state:
    st.session_state.genero_f = ""
if 'fecha_f' not in st.session_state:
    st.session_state.fecha_f = ""
if 'cui' not in st.session_state:
    st.session_state.cui = ""
if 'empresa_fill' not in st.session_state:
    st.session_state.empresa_fill = ""
if 'email_fill' not in st.session_state:
    st.session_state.email_fill = ""
if 'puesto_fill' not in st.session_state:
    st.session_state.puesto_fill = ""
#======================================================================================
#======================================================================================
#st.title("Cualquier otra imagen...")
st.image("https://i.imgur.com/h9VvPUe.png")
st.markdown("***")
#======================================================================================
#======================================================================================
st.sidebar.title("Bienvenido")
user = st.sidebar.radio("Seleccionar", ["Nuevo colaborador", "Actualización datos"])
#======================================================================================
#======================================================================================
rrhh_email = ["rehumanos@tppemarketing.com","rcastro@tppemarketing.com"]
rrhh_pass = "123"
if user == "Nuevo colaborador":
    st.sidebar.success("Uso exclusivo de RRHH")
    email_rrhh = st.sidebar.text_input("Ingresar correo RRHH")
    pass_rrhh = st.sidebar.text_input("Ingresar password", type = "password")
    
    if ((email_rrhh == rrhh_email[0] or email_rrhh == rrhh_email[1]) and (pass_rrhh == rrhh_pass)):
        st.subheader("Agregar información colaborador")
        add_user = st.expander("Formulario", expanded = True)
        with add_user:
            st.markdown("###### Información general")
            c_1, c_2, c_3 = st.columns(3)
            nombres = c_1.text_input("Nombres")
            apellidos = c_1.text_input("Apellidos")
            genero = c_1.selectbox("Género", ["F", "M"])
            fecha = c_2.date_input("Fecha de nacimiento - YY/MM/DD")
            cui = c_2.text_input("CUI (no guiones ni espacios)")
            empresa = c_3.multiselect("Empresa/Hub", e_hub)
            email = c_3.text_input("Correo Electrónico")
            puesto = c_3.multiselect("Puesto", nombre_puesto)
            st.markdown("***")
            #===================================================================
            #===================================================================
            st.markdown("###### Educación")
            c_4, c_5, c_6, c_7 = st.columns(4)
            with c_4:
                with st.form("Diversificado", clear_on_submit = True):
                    st.markdown("###### Diversificado")
                    st.markdown("######  ")
                    lugar_d = st.text_input("Lugar")
                    titulo_d = st.text_input("Título obtenido")
                    e_d = st.selectbox("Estado", ["Terminado", "Cierre de Pensum", "En Curso"])
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    if st.form_submit_button("Agregar"):
                        st.session_state.lugar_d.append(lugar_d)
                        st.session_state.titulo_d.append(titulo_d)
                        st.session_state.e_d.append(e_d)
            with c_5:
                with st.form("Licenciatura", clear_on_submit = True):
                    st.markdown("###### Licenciatura")
                    st.markdown("######  ")
                    lugar_l = st.text_input("Lugar")
                    titulo_l = st.text_input("Título obtenido")
                    e_l = st.selectbox("Estado", ["N/A","Terminado", "Cierre de Pensum", "En Curso"])
                    semestre = st.number_input("Semestre", 0, 12)
                    if st.form_submit_button("Agregar"):
                        st.session_state.lugar_l.append(lugar_l)
                        st.session_state.titulo_l.append(titulo_l)
                        st.session_state.e_l.append(e_l)
                        st.session_state.e_ll.append(semestre)
            with c_6:
                with st.form("Maestria", clear_on_submit = True):
                    st.markdown("###### Maestría/Posgrado")
                    st.markdown("######  ")
                    lugar_m = st.text_input("Lugar")
                    titulo_m = st.text_input("Título obtenido")
                    e_m = st.selectbox("Estado", ["N/A","Terminado", "Cierre de Pensum", "En Curso"])
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    if st.form_submit_button("Agregar"):
                        st.session_state.lugar_m.append(lugar_m)
                        st.session_state.titulo_m.append(titulo_m)
                        st.session_state.e_m.append(e_m)
            with c_7:
                with st.form("Cursos", clear_on_submit = True):
                    st.markdown("###### Cursos/Diplomados/Certificaciones")
                    lugar_c = st.text_input("Lugar")
                    titulo_c = st.text_input("Nombre")
                    e_c = st.selectbox("Estado", ["N/A","Terminado", "En Curso"])
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    if st.form_submit_button("Agregar"):
                        st.session_state.lugar_c.append(lugar_c)
                        st.session_state.titulo_c.append(titulo_c)
                        st.session_state.e_c.append(e_c)
            #===================================================================
            #===================================================================
            if st.checkbox("Vista previa información", key = 2):
                st.markdown("###### Información General")
                c_11, c_22, c_33 = st.columns(3)
                with c_11:
                    st.markdown("Nombres")
                    st.success(nombres)
                    st.markdown("Apellidos")
                    st.success(apellidos)
                    st.markdown("Género")
                    st.success(genero)
                with c_22:
                    st.markdown("Fecha de Nacimiento")
                    st.success(str(fecha))
                    st.markdown("CUI")
                    st.success(cui)
                with c_33:
                    st.markdown("Empresa/Hub")
                    st.success(", ".join(empresa))
                    st.markdown("Correo Electrónico")
                    st.success(email)
                    st.markdown("Puesto")
                    st.success(", ".join(puesto))
                st.markdown("***")
                st.markdown("###### Educación")
                c_44, c_55, c_66, c_77 = st.columns(4)
                with c_44:
                    st.markdown("###### Diversificado")
                    st.markdown("")
                    df_44 = pd.DataFrame(list(zip(st.session_state.lugar_d, st.session_state.titulo_d, st.session_state.e_d)), columns = ["Lugar", "Título obtenido", "Estado"])
                    fig = go.Figure(data=[go.Table(header=dict(values=list(df_44.columns), fill_color='paleturquoise', align='left'), cells=dict(values=[df_44["Lugar"], df_44["Título obtenido"], df_44["Estado"]], fill_color='lavender', align='left'))])
                    fig.update_layout(height = 50 + 50*len(df_44), margin=dict(r=1, l=1, t=1, b=0, pad = 4))
                    st.plotly_chart(fig, use_container_width=True)
                with c_55:
                    st.markdown("###### Licenciatura")
                    st.markdown("")
                    df_55 = pd.DataFrame(list(zip(st.session_state.lugar_l, st.session_state.titulo_l, st.session_state.e_l, st.session_state.e_ll)), columns = ["Lugar", "Título obtenido", "Estado", "Semestre"])
                    fig = go.Figure(data=[go.Table(header=dict(values=list(df_44.columns), fill_color='paleturquoise', align='left'), cells=dict(values=[df_55["Lugar"], df_55["Título obtenido"], df_55["Estado"]], fill_color='lavender', align='left'))])
                    fig.update_layout(height = 50 + 50*len(df_55),margin=dict(r=1, l=1, t=1, b=0))
                    st.plotly_chart(fig, use_container_width=True)
                with c_66:
                    st.markdown("###### Maestría/Posgrado")
                    st.markdown("")
                    df_66 = pd.DataFrame(list(zip(st.session_state.lugar_m, st.session_state.titulo_m, st.session_state.e_m)), columns = ["Lugar", "Título obtenido", "Estado"])
                    fig = go.Figure(data=[go.Table(header=dict(values=list(df_66.columns), fill_color='paleturquoise', align='left'), cells=dict(values=[df_66["Lugar"], df_66["Título obtenido"], df_66["Estado"]], fill_color='lavender', align='left'))])
                    fig.update_layout(height = 50 + 50*len(df_66),margin=dict(r=1, l=1, t=1, b=0))
                    st.plotly_chart(fig, use_container_width=True)
                with c_77:
                    st.markdown("###### Cursos/Diplomados/Certificaciones")
                    df_77 = pd.DataFrame(list(zip(st.session_state.lugar_c, st.session_state.titulo_c, st.session_state.e_c)), columns = ["Lugar", "Título obtenido", "Estado"])
                    fig = go.Figure(data=[go.Table(header=dict(values=list(df_77.columns), fill_color='paleturquoise', align='left'), cells=dict(values=[df_77["Lugar"], df_77["Título obtenido"], df_77["Estado"]], fill_color='lavender', align='left'))])
                    fig.update_layout(height = 50 + 50*len(df_77),margin=dict(r=1, l=1, t=1, b=0))
                    st.plotly_chart(fig, use_container_width=True)
            #===================================================================
            #===================================================================
            if st.button("Guardar Información", key = 1):
                df = st.session_state.spread.sheet_to_df()
                df_append = pd.DataFrame([[nombres, apellidos, genero, fecha, cui, empresa, email, puesto, st.session_state.lugar_d, st.session_state.titulo_d, st.session_state.e_d, st.session_state.lugar_l, st.session_state.titulo_l, st.session_state.e_l, st.session_state.e_ll, st.session_state.lugar_m, st.session_state.titulo_m, st.session_state.e_m, st.session_state.lugar_c, st.session_state.titulo_c, st.session_state.e_c]], columns = name_columns)
                df = pd.concat([df, df_append], axis = 0)
                st.session_state.spread.df_to_sheet(df, index = False)
                st.session_state.lugar_d = []
                st.session_state.titulo_d = []
                st.session_state.e_d = []
                st.session_state.lugar_l = []
                st.session_state.titulo_l = []
                st.session_state.e_l = []
                st.session_state.e_ll = []
                st.session_state.lugar_m = []
                st.session_state.titulo_m = []
                st.session_state.e_m = []
                st.session_state.lugar_c = []
                st.session_state.titulo_c = []
                st.session_state.e_c = []
                st.balloons()
#======================================================================================
#======================================================================================
if user == "Actualización datos":
    email_prefill = st.sidebar.text_input("Ingresar correo")
    cui_prefill = st.sidebar.text_input("Ingresar CUI (sin espacios ni guiones)", type = "password")
    if email_prefill and cui_prefill:
        info = df[df["Email"] == email_prefill].tail(1)
        if info["CUI"].values[0] != cui_prefill:
            st.sidebar.error("Credenciales incorrectas")
        else:
            st.sidebar.success("Puede consultar su información")
            add_user_f = st.expander("Formulario - Actualización", expanded = True)
            with add_user_f:
                st.markdown("###### Información general")
                #------------------------------------
                #------------------------------------
                if st.session_state.count_pi_ag == 1:
                    st.session_state.nombres_f = info["Nombres"].values[0]
                    st.session_state.apellidos_f = info["Apellidos"].values[0]
                    st.session_state.genero_f = info["Género"].values[0]
                    st.session_state.fecha_f = info["Fecha de Nacimiento"].values[0]
                    st.session_state.cui = info["CUI"].values[0]
                    st.session_state.empresa_fill = eval(info["Empresa/Hub"].values[0])
                    st.session_state.email_fill = info["Email"].values[0]
                    st.session_state.puesto_fill = eval(info["Puesto"].values[0])
                #------------------------------------
                #------------------------------------
                #Jalar datos para llenar los forms
                if st.session_state.count_pi_ac == 1 and st.session_state.n_b_d == False:
                    st.session_state.lugar_d = eval(info["Lugar Diversificado"].values[0])
                    st.session_state.titulo_d = eval(info["Nombre Diversificado"].values[0])
                    st.session_state.e_d = eval(info["Estado Diversificado"].values[0])
                #------------------------------------
                if st.session_state.count_pi_al == 1 and st.session_state.n_b_d == False:
                    st.session_state.lugar_l = eval(info["Lugar Licenciatura"].values[0])
                    st.session_state.titulo_l = eval(info["Nombre Licenciatura"].values[0])
                    st.session_state.e_l = eval(info["Estado Licenciatura"].values[0])
                    st.session_state.e_ll = eval(info["Semestre"].values[0])
                #------------------------------------
                if st.session_state.count_pi_am == 1 and st.session_state.n_b_d == False:
                    st.session_state.lugar_m = eval(info["Lugar Maestría/Posgrado"].values[0])
                    st.session_state.titulo_m = eval(info["Nombre Maestría/Posgrado"].values[0])
                    st.session_state.e_m = eval(info["Estado Maestría/Posgrado"].values[0])
                #------------------------------------
                if st.session_state.count_pi_acc == 1 and st.session_state.n_b_d == False:
                    st.session_state.lugar_c = eval(info["Lugar Cursos/Diplomados/Certificaciones"].values[0])
                    st.session_state.titulo_c = eval(info["Nombre Cursos/Diplomados/Certificaciones"].values[0])
                    st.session_state.e_c = eval(info["Estado Cursos/Diplomados/Certificaciones"].values[0])
                #------------------------------------
                #------------------------------------
                c_1_f, c_2_f, c_3_f = st.columns(3)
                #Placeholders columna c_1_f
                pp_nombre = c_1_f.empty()
                p_nombre = c_1_f.empty()
                pp_apellido = c_1_f.empty()
                p_apellido = c_1_f.empty()
                pp_genero = c_1_f.empty()
                p_genero = c_1_f.empty()
                #Placeholders columna c_2_f
                pp_fecha = c_2_f.empty()
                p_fecha = c_2_f.empty()
                pp_CUI = c_2_f.empty()
                p_CUI = c_2_f.empty()
                #Placeholders columna c_3_f
                pp_empresa = c_3_f.empty()
                p_empresa = c_3_f.empty()
                pp_correo = c_3_f.empty()
                p_correo = c_3_f.empty()
                pp_puesto = c_3_f.empty()
                p_puesto = c_3_f.empty()
                #------------------------------------
                #------------------------------------
                boton = st.button("Actualizar Información General")
                if boton:
                    st.session_state.count_pi_ag += 1
                if st.session_state.count_pi_ag % 2 == 0:
                    st.session_state.nombres_f = p_nombre.text_input("Nombres", st.session_state.nombres_f)
                    st.session_state.apellidos_f = p_apellido.text_input("Apellidos", st.session_state.apellidos_f)
                    ff_gen = ["F", "M"]
                    if st.session_state.genero_f == "F":
                        gender_index = 0
                    else:
                        gender_index = 1
                    st.session_state.genero_f = p_genero.selectbox("Género", ff_gen, index = gender_index, key = "genero_ff")
                    print(st.session_state.genero_f)
                    st.session_state.fecha_f = p_fecha.date_input("Fecha de nacimiento - YY/MM/DD", key = "fecha_fill", value = datetime.strptime(str(st.session_state.fecha_f), '%Y-%m-%d'))
                    pp_CUI.markdown("CUI")
                    p_CUI.info(st.session_state.cui)
                    st.session_state.empresa_fill = p_empresa.multiselect("Empresa/Hub", e_hub, default = st.session_state.empresa_fill)
                    pp_correo.markdown("Correo Electrónico")
                    p_correo.info(st.session_state.email_fill)
                    st.session_state.puesto_fill = p_puesto.multiselect("Puesto", nombre_puesto, st.session_state.puesto_fill)
                else:
                    pp_nombre.markdown("Nombres")
                    p_nombre.info(st.session_state.nombres_f)
                    pp_apellido.markdown("Apellidos")
                    p_apellido.info(st.session_state.apellidos_f)
                    pp_genero.markdown("Género")
                    p_genero.info(st.session_state.genero_f)
                    pp_fecha.markdown("Fecha de Nacimiento")
                    p_fecha.info(str(st.session_state.fecha_f))
                    pp_CUI.markdown("CUI")
                    p_CUI.info(st.session_state.cui)
                    pp_empresa.markdown("Empresa/Hub")
                    p_empresa.info(", ".join(st.session_state.empresa_fill))
                    pp_correo.markdown("Correo Electrónico")
                    p_correo.info(st.session_state.email_fill)
                    pp_puesto.markdown("Puesto")
                    p_puesto.info(", ".join(st.session_state.puesto_fill))
                #------------------------------------
                #------------------------------------
                st.markdown("***")
                st.markdown("###### Educación")
                c_4_f, c_5_f, c_6_f, c_7_f = st.columns(4)
                #Placeholders columna c_4_f
                #------------------------------------
                #------------------------------------
                with c_4_f:
                    form_4_f = st.form("Diversificado", clear_on_submit = True)
                    form_4_f.markdown("###### Diversificado")
                    form_4_f.markdown("######  ")
                    form_4_f.markdown("######  ")
                    pp_lugar_d = form_4_f.empty()
                    p_lugar_d = form_4_f.empty()
                    pp_nombre_d = form_4_f.empty()
                    p_nombre_d = form_4_f.empty()
                    pp_estado_d = form_4_f.empty()
                    p_estado_d = form_4_f.empty()
                    #------------------------------------
                    form_4_f.markdown("##### ")
                    form_4_f.markdown("")
                    form_4_f.markdown("")
                    form_4_f.markdown("")
                    form_4_f.markdown("")
                    form_4_f.markdown("")
                    form_4_f.markdown("")
                    change_button_form_4_f = form_4_f.form_submit_button("Actualizar")
                    if (change_button_form_4_f and st.session_state.explorar == "Diversificado"):
                        st.session_state.count_pi_ac += 1
                        st.session_state.p_explorar = st.session_state.explorar
                        st.session_state.lugar_d[st.session_state.count_ac] = p_lugar_d.text_input("Lugar", st.session_state.lugar_d[st.session_state.count_ac])
                        st.session_state.titulo_d[st.session_state.count_ac] = p_nombre_d.text_input("Título obtenido", st.session_state.titulo_d[st.session_state.count_ac])
                        f_ed = ["N/A","Terminado", "Cierre de Pensum", "En Curso"]
                        st.session_state.e_d[st.session_state.count_ac] = p_estado_d.selectbox("Estado", f_ed, index = f_ed.index(st.session_state.e_d[st.session_state.count_ac]))
                    if st.session_state.count_pi_ac % 2 != 0:
                        pp_lugar_d.markdown("Lugar")
                        p_lugar_d.info(st.session_state.lugar_d[st.session_state.count_ac])
                        pp_nombre_d.markdown("Título obtenido")
                        p_nombre_d.info(st.session_state.titulo_d[st.session_state.count_ac])
                        pp_estado_d.markdown("Estado")
                        p_estado_d.info(st.session_state.e_d[st.session_state.count_ac])
                    
                #------------------------------------
                #------------------------------------
                with c_5_f:
                    form_5_f = st.form("Licenciatura", clear_on_submit = True)
                    form_5_f.markdown("###### Licenciatura")
                    form_5_f.markdown("######  ")
                    form_5_f.markdown("######  ")
                    pp_lugar_l = form_5_f.empty()
                    p_lugar_l = form_5_f.empty()
                    pp_nombre_l = form_5_f.empty()
                    p_nombre_l = form_5_f.empty()
                    pp_estado_l = form_5_f.empty()
                    p_estado_l = form_5_f.empty()
                    pp_semestre_l = form_5_f.empty()
                    p_semestre_l = form_5_f.empty()
                    #------------------------------------
                    change_button_form_5_f = form_5_f.form_submit_button("Actualizar")
                    if (change_button_form_5_f and st.session_state.explorar == "Licenciatura"):
                        st.session_state.count_pi_al += 1
                        st.session_state.p_explorar = st.session_state.explorar
                        st.session_state.lugar_l[st.session_state.count_al] = p_lugar_l.text_input("Lugar", st.session_state.lugar_l[st.session_state.count_al])
                        st.session_state.titulo_l[st.session_state.count_al] = p_nombre_l.text_input("Título obtenido", st.session_state.titulo_l[st.session_state.count_al])
                        f_el = ["N/A","Terminado", "Cierre de Pensum", "En Curso"]
                        st.session_state.e_l[st.session_state.count_al] = p_estado_l.selectbox("Estado", f_el, index = f_el.index(st.session_state.e_l[st.session_state.count_al]))
                        st.session_state.e_ll[st.session_state.count_al] = p_semestre_l.number_input("Semestre", 0, 12, value = st.session_state.e_ll[st.session_state.count_al])
                    if st.session_state.count_pi_al % 2 != 0:
                        pp_lugar_l.markdown("Lugar")
                        p_lugar_l.info(st.session_state.lugar_l[st.session_state.count_al])
                        pp_nombre_l.markdown("Título obtenido")
                        p_nombre_l.info(st.session_state.titulo_l[st.session_state.count_al])
                        pp_estado_l.markdown("Estado")
                        p_estado_l.info(st.session_state.e_l[st.session_state.count_al])
                        pp_semestre_l.markdown("Semestre")
                        p_semestre_l.info(st.session_state.e_ll[st.session_state.count_al])
                #------------------------------------
                #------------------------------------
                with c_6_f:
                    form_6_f = st.form("Maestria", clear_on_submit = True)
                    form_6_f.markdown("###### Maestría/Posgrado")
                    form_6_f.markdown("######  ")
                    form_6_f.markdown("######  ")
                    pp_lugar_m = form_6_f.empty()
                    p_lugar_m = form_6_f.empty()
                    pp_nombre_m = form_6_f.empty()
                    p_nombre_m = form_6_f.empty()
                    pp_estado_m = form_6_f.empty()
                    p_estado_m = form_6_f.empty()
                    #------------------------------------
                    form_6_f.markdown("##### ")
                    form_6_f.markdown("")
                    form_6_f.markdown("")
                    form_6_f.markdown("")
                    form_6_f.markdown("")
                    form_6_f.markdown("")
                    form_6_f.markdown("")
                    change_button_form_6_f = form_6_f.form_submit_button("Actualizar")
                    if (change_button_form_6_f and st.session_state.explorar == "Maestría/Posgrado"):
                        st.session_state.count_pi_am += 1
                        st.session_state.p_explorar = st.session_state.explorar
                        st.session_state.lugar_m[st.session_state.count_am] = p_lugar_m.text_input("Lugar", st.session_state.lugar_m[st.session_state.count_am])
                        st.session_state.titulo_m[st.session_state.count_am] = p_nombre_m.text_input("Título obtenido", st.session_state.titulo_m[st.session_state.count_am])
                        f_em = ["N/A","Terminado", "Cierre de Pensum", "En Curso"]
                        st.session_state.e_m[st.session_state.count_am] = p_estado_m.selectbox("Estado", f_em, index = f_em.index(st.session_state.e_m[st.session_state.count_am]))
                    if st.session_state.count_pi_am % 2 != 0:
                        pp_lugar_m.markdown("Lugar")
                        p_lugar_m.info(st.session_state.lugar_m[st.session_state.count_am])
                        pp_nombre_m.markdown("Título obtenido")
                        p_nombre_m.info(st.session_state.titulo_m[st.session_state.count_am])
                        pp_estado_m.markdown("Estado")
                        p_estado_m.info(st.session_state.e_m[st.session_state.count_am])
                #------------------------------------
                #------------------------------------
                with c_7_f:
                    form_7_f = st.form("Cursos/Diplomados/Certificaciones", clear_on_submit = True)
                    form_7_f.markdown("###### Cursos/Diplomados/Certificaciones")
                    form_7_f.markdown("######  ")
                    pp_lugar_c = form_7_f.empty()
                    p_lugar_c = form_7_f.empty()
                    pp_nombre_c = form_7_f.empty()
                    p_nombre_c = form_7_f.empty()
                    pp_estado_c = form_7_f.empty()
                    p_estado_c = form_7_f.empty()
                    #------------------------------------
                    form_7_f.markdown("##### ")
                    form_7_f.markdown("")
                    form_7_f.markdown("")
                    form_7_f.markdown("")
                    form_7_f.markdown("")
                    form_7_f.markdown("")
                    form_7_f.markdown("")
                    change_button_form_7_f = form_7_f.form_submit_button("Actualizar")
                    if (change_button_form_7_f and st.session_state.explorar == "Cursos/Diplomados/Certificaciones"):
                        st.session_state.count_pi_acc += 1
                        st.session_state.p_explorar = st.session_state.explorar
                        st.session_state.lugar_c[st.session_state.count_acc] = p_lugar_c.text_input("Lugar", st.session_state.lugar_c[st.session_state.count_acc])
                        st.session_state.titulo_c[st.session_state.count_acc] = p_nombre_c.text_input("Título obtenido", st.session_state.titulo_c[st.session_state.count_acc])
                        f_ec = ["N/A","Terminado", "Cierre de Pensum", "En Curso"]
                        st.session_state.e_c[st.session_state.count_acc] = p_estado_c.selectbox("Estado", f_ec, index = f_ec.index(st.session_state.e_c[st.session_state.count_acc]))
                    if st.session_state.count_pi_acc % 2 != 0:
                        pp_lugar_c.markdown("Lugar")
                        p_lugar_c.info(st.session_state.lugar_c[st.session_state.count_acc])
                        pp_nombre_c.markdown("Título obtenido")
                        p_nombre_c.info(st.session_state.titulo_c[st.session_state.count_acc])
                        pp_estado_c.markdown("Estado")
                        p_estado_c.info(st.session_state.e_c[st.session_state.count_acc])
                
                c_4_m, c_5_m, c_6_m, c_7_m = st.columns(4)
                with c_4_m:
                    metric_d = c_4_m.empty()
                    metric_d.metric(label="Página #", value = st.session_state.count_ac + 1, delta = len(st.session_state.lugar_d), delta_color="off")
                with c_5_m:
                    metric_l = c_5_m.empty()
                    metric_l.metric(label="Página #", value = st.session_state.count_al + 1, delta = len(st.session_state.lugar_l), delta_color="off")
                with c_6_m:
                    metric_m = c_6_m.empty()
                    metric_m.metric(label="Página #", value = st.session_state.count_am + 1, delta = len(st.session_state.lugar_m), delta_color="off")
                with c_7_m:
                    metric_acc = c_7_m.empty()
                    metric_acc.metric(label="Página #", value = st.session_state.count_acc + 1, delta = len(st.session_state.lugar_c), delta_color="off")
                #------------------------------------
                #------------------------------------
                c_aaa, c_bbb, c_ccc= st.columns([2,1,1])
                with c_aaa:
                    st.markdown("#### Explorar registros")
                    st.session_state.explorar = st.selectbox("", ["Diversificado", "Licenciatura", "Maestría/Posgrado", "Cursos/Diplomados/Certificaciones"])
                    if st.session_state.count_pi_ac % 2 == 0 and st.session_state.p_explorar != st.session_state.explorar:
                        pp_lugar_d.markdown("Lugar")
                        p_lugar_d.info(st.session_state.lugar_d[st.session_state.count_ac])
                        pp_nombre_d.markdown("Título obtenido")
                        p_nombre_d.info(st.session_state.titulo_d[st.session_state.count_ac])
                        pp_estado_d.markdown("Estado")
                        p_estado_d.info(st.session_state.e_d[st.session_state.count_ac])
                        st.session_state.count_pi_ac += 1
                    if st.session_state.count_pi_al % 2 == 0 and st.session_state.p_explorar != st.session_state.explorar:
                        pp_lugar_l.markdown("Lugar")
                        p_lugar_l.info(st.session_state.lugar_l[st.session_state.count_al])
                        pp_nombre_l.markdown("Título obtenido")
                        p_nombre_l.info(st.session_state.titulo_l[st.session_state.count_al])
                        pp_estado_l.markdown("Estado")
                        p_estado_l.info(st.session_state.e_l[st.session_state.count_al])
                        pp_semestre_l.markdown("Semestre")
                        p_semestre_l.info(st.session_state.e_ll[st.session_state.count_al])
                        st.session_state.count_pi_al += 1
                    if st.session_state.count_pi_am % 2 == 0 and st.session_state.p_explorar != st.session_state.explorar:
                        pp_lugar_m.markdown("Lugar")
                        p_lugar_m.info(st.session_state.lugar_m[st.session_state.count_am])
                        pp_nombre_m.markdown("Título obtenido")
                        p_nombre_m.info(st.session_state.titulo_m[st.session_state.count_am])
                        pp_estado_m.markdown("Estado")
                        p_estado_m.info(st.session_state.e_m[st.session_state.count_am])
                        st.session_state.count_pi_am += 1
                    if st.session_state.count_pi_acc % 2 == 0 and st.session_state.p_explorar != st.session_state.explorar:
                        pp_lugar_c.markdown("Lugar")
                        p_lugar_c.info(st.session_state.lugar_c[st.session_state.count_acc])
                        pp_nombre_c.markdown("Título obtenido")
                        p_nombre_c.info(st.session_state.titulo_c[st.session_state.count_acc])
                        pp_estado_c.markdown("Estado")
                        p_estado_c.info(st.session_state.e_c[st.session_state.count_acc])
                        st.session_state.count_pi_acc += 1
                with c_ccc:
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    guardar_all = st.button("Guardar todos los cambios")
                    if guardar_all:
                        df = st.session_state.spread.sheet_to_df()
                        df_append = pd.DataFrame([[st.session_state.nombres_f, st.session_state.apellidos_f, st.session_state.genero_f, st.session_state.fecha_f, st.session_state.cui, st.session_state.empresa_fill, st.session_state.email_fill, st.session_state.puesto_fill, st.session_state.lugar_d, st.session_state.titulo_d, st.session_state.e_d, st.session_state.lugar_l, st.session_state.titulo_l, st.session_state.e_l, st.session_state.e_ll, st.session_state.lugar_m, st.session_state.titulo_m, st.session_state.e_m, st.session_state.lugar_c, st.session_state.titulo_c, st.session_state.e_c]], columns = name_columns)
                        df = pd.concat([df, df_append], axis = 0)
                        st.session_state.spread.df_to_sheet(df, index = False)
                        st.balloons()
                
                c_aa, c_bb, c_cc, c_dd, c_ee, c_ff, c_gg, c_hh, c_ii, c_jj, c_kk, c_ll = st.columns([1,1.5,1,1,1,1,1,1,1,1,1,1])
                
                with c_aa:
                    b_aa = st.button("<")
                    if (b_aa and st.session_state.count_ac > 0 and st.session_state.explorar == "Diversificado"):
                        st.session_state.count_ac -= 1
                        pp_lugar_d.markdown("Lugar")
                        p_lugar_d.info(st.session_state.lugar_d[st.session_state.count_ac])
                        pp_nombre_d.markdown("Título obtenido")
                        p_nombre_d.info(st.session_state.titulo_d[st.session_state.count_ac])
                        pp_estado_d.markdown("Estado")
                        p_estado_d.info(st.session_state.e_d[st.session_state.count_ac])
                        metric_d.metric(label="Página #", value = st.session_state.count_ac + 1, delta = len(st.session_state.lugar_d), delta_color="off")
                    if (b_aa and st.session_state.count_al > 0 and st.session_state.explorar == "Licenciatura"):
                        st.session_state.count_al -= 1
                        pp_lugar_l.markdown("Lugar")
                        p_lugar_l.info(st.session_state.lugar_l[st.session_state.count_al])
                        pp_nombre_l.markdown("Título obtenido")
                        p_nombre_l.info(st.session_state.titulo_l[st.session_state.count_al])
                        pp_estado_l.markdown("Estado")
                        p_estado_l.info(st.session_state.e_l[st.session_state.count_al])
                        pp_semestre_l.markdown("Semestre")
                        p_semestre_l.info(st.session_state.e_ll[st.session_state.count_al])
                        metric_l.metric(label="Página #", value = st.session_state.count_al + 1, delta = len(st.session_state.lugar_l), delta_color="off")
                    if (b_aa and st.session_state.count_am > 0 and st.session_state.explorar == "Maestría/Posgrado"):
                        st.session_state.count_am -= 1
                        pp_lugar_m.markdown("Lugar")
                        p_lugar_m.info(st.session_state.lugar_m[st.session_state.count_am])
                        pp_nombre_m.markdown("Título obtenido")
                        p_nombre_m.info(st.session_state.titulo_m[st.session_state.count_am])
                        pp_estado_m.markdown("Estado")
                        p_estado_m.info(st.session_state.e_m[st.session_state.count_am])
                        metric_m.metric(label="Página #", value = st.session_state.count_am + 1, delta = len(st.session_state.lugar_m), delta_color="off")
                    if (b_aa and st.session_state.count_acc > 0 and st.session_state.explorar == "Cursos/Diplomados/Certificaciones"):
                        st.session_state.count_acc -= 1
                        pp_lugar_c.markdown("Lugar")
                        p_lugar_c.info(st.session_state.lugar_c[st.session_state.count_acc])
                        pp_nombre_c.markdown("Título obtenido")
                        p_nombre_c.info(st.session_state.titulo_c[st.session_state.count_acc])
                        pp_estado_c.markdown("Estado")
                        p_estado_c.info(st.session_state.e_c[st.session_state.count_acc])
                        metric_acc.metric(label="Página #", value = st.session_state.count_acc + 1, delta = len(st.session_state.lugar_c), delta_color="off")
                with c_bb:
                    b_bb = st.button("Nuevo")
                    if (b_bb and st.session_state.explorar == "Diversificado"):
                        st.session_state.n_b_d = True
                        pp_lugar_d.empty()
                        pp_nombre_d.empty()
                        pp_estado_d.empty()
                        st.session_state.lugar_d.append("")
                        st.session_state.titulo_d.append("")
                        st.session_state.e_d.append("N/A")
                        pp_lugar_d.markdown("Lugar")
                        p_lugar_d.info(st.session_state.lugar_d[-1])
                        pp_nombre_d.markdown("Título obtenido")
                        p_nombre_d.info(st.session_state.titulo_d[-1])
                        pp_nombre_d.markdown("Estado")
                        p_estado_d.info(st.session_state.e_d[-1])
                        st.session_state.count_ac = len(st.session_state.lugar_d) - 1
                        metric_d.metric(label="Página #", value = st.session_state.count_ac + 1, delta = len(st.session_state.lugar_d), delta_color="off")
                    elif (b_bb and st.session_state.explorar == "Licenciatura"):
                        st.session_state.n_b_d = True
                        pp_lugar_l.empty()
                        pp_nombre_l.empty()
                        pp_estado_l.empty()
                        pp_semestre_l.empty()
                        st.session_state.lugar_l.append("")
                        st.session_state.titulo_l.append("")
                        st.session_state.e_l.append("N/A")
                        st.session_state.e_ll.append(0)
                        pp_lugar_l.markdown("Lugar")
                        p_lugar_l.info(st.session_state.lugar_l[-1])
                        pp_nombre_l.markdown("Título obtenido")
                        p_nombre_l.info(st.session_state.titulo_l[-1])
                        pp_estado_l.markdown("Estado")
                        p_estado_l.info(st.session_state.e_l[-1])
                        pp_semestre_l.markdown("Semestre")
                        p_semestre_l.info(st.session_state.e_ll[-1])
                        st.session_state.count_al = len(st.session_state.lugar_l) - 1
                        metric_l.metric(label="Página #", value = st.session_state.count_al + 1, delta = len(st.session_state.lugar_l), delta_color="off")
                    elif (b_bb and st.session_state.explorar == "Maestría/Posgrado"):
                        st.session_state.n_b_d = True
                        pp_lugar_m.empty()
                        pp_nombre_m.empty()
                        pp_estado_m.empty()
                        st.session_state.lugar_m.append("")
                        st.session_state.titulo_m.append("")
                        st.session_state.e_m.append("N/A")
                        pp_lugar_m.markdown("Lugar")
                        p_lugar_m.info(st.session_state.lugar_m[-1])
                        pp_nombre_m.markdown("Título obtenido")
                        p_nombre_m.info(st.session_state.titulo_m[-1])
                        pp_estado_m.markdown("Estado")
                        p_estado_m.info(st.session_state.e_m[-1])
                        st.session_state.count_am = len(st.session_state.lugar_m) - 1
                        metric_m.metric(label="Página #", value = st.session_state.count_am + 1, delta = len(st.session_state.lugar_m), delta_color="off")
                    elif (b_bb and st.session_state.explorar == "Cursos/Diplomados/Certificaciones"):
                        st.session_state.n_b_d = True
                        pp_lugar_c.empty()
                        pp_nombre_c.empty()
                        pp_estado_c.empty()
                        st.session_state.lugar_c.append("")
                        st.session_state.titulo_c.append("")
                        st.session_state.e_c.append("N/A")
                        pp_lugar_c.markdown("Lugar")
                        p_lugar_c.info(st.session_state.lugar_c[-1])
                        pp_nombre_c.markdown("Título obtenido")
                        p_nombre_c.info(st.session_state.titulo_c[-1])
                        pp_estado_c.markdown("Estado")
                        p_estado_c.info(st.session_state.e_c[-1])
                        st.session_state.count_acc = len(st.session_state.lugar_c) - 1
                        metric_acc.metric(label="Página #", value = st.session_state.count_acc + 1, delta = len(st.session_state.lugar_c), delta_color="off")
                with c_cc:
                    b_cc = st.button(">")
                    if (b_cc and st.session_state.count_ac < (len(st.session_state.lugar_d)-1)  and st.session_state.explorar == "Diversificado"):
                        st.session_state.count_ac += 1
                        pp_lugar_d.markdown("Lugar")
                        p_lugar_d.info(st.session_state.lugar_d[st.session_state.count_ac])
                        pp_nombre_d.markdown("Título obtenido")
                        p_nombre_d.info(st.session_state.titulo_d[st.session_state.count_ac])
                        pp_estado_d.markdown("Estado")
                        p_estado_d.info(st.session_state.e_d[st.session_state.count_ac])
                        metric_d.metric(label="Página #", value = st.session_state.count_ac + 1, delta = len(st.session_state.lugar_d), delta_color="off")
                    if (b_cc and st.session_state.count_al < (len(st.session_state.lugar_l)-1)  and st.session_state.explorar == "Licenciatura"):
                        st.session_state.count_al += 1
                        pp_lugar_l.markdown("Lugar")
                        p_lugar_l.info(st.session_state.lugar_l[st.session_state.count_al])
                        pp_nombre_l.markdown("Título obtenido")
                        p_nombre_l.info(st.session_state.titulo_l[st.session_state.count_al])
                        pp_estado_l.markdown("Estado")
                        p_estado_l.info(st.session_state.e_l[st.session_state.count_al])
                        pp_semestre_l.markdown("Semestre")
                        p_semestre_l.info(st.session_state.e_ll[st.session_state.count_al])
                        metric_l.metric(label="Página #", value = st.session_state.count_al + 1, delta = len(st.session_state.lugar_l), delta_color="off")
                    if (b_cc and st.session_state.count_am < (len(st.session_state.lugar_m)-1)  and st.session_state.explorar == "Maestría/Posgrado"):
                        st.session_state.count_am += 1
                        pp_lugar_m.markdown("Lugar")
                        p_lugar_m.info(st.session_state.lugar_m[st.session_state.count_am])
                        pp_nombre_m.markdown("Título obtenido")
                        p_nombre_m.info(st.session_state.titulo_m[st.session_state.count_am])
                        pp_estado_m.markdown("Estado")
                        p_estado_m.info(st.session_state.e_m[st.session_state.count_am])
                        metric_m.metric(label="Página #", value = st.session_state.count_am + 1, delta = len(st.session_state.lugar_m), delta_color="off")
                    if (b_cc and st.session_state.count_acc < (len(st.session_state.lugar_c)-1)  and st.session_state.explorar == "Cursos/Diplomados/Certificaciones"):
                        st.session_state.count_acc += 1
                        pp_lugar_c.markdown("Lugar")
                        p_lugar_c.info(st.session_state.lugar_c[st.session_state.count_acc])
                        pp_nombre_c.markdown("Título obtenido")
                        p_nombre_c.info(st.session_state.titulo_c[st.session_state.count_acc])
                        pp_estado_c.markdown("Estado")
                        p_estado_c.info(st.session_state.e_c[st.session_state.count_acc])
                        metric_acc.metric(label="Página #", value = st.session_state.count_acc + 1, delta = len(st.session_state.lugar_c), delta_color="off")
    #===================================================================
    #===================================================================
