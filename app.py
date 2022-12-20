import streamlit as st




######################################
st.warning("Assicurati di aver settato l'asse Z  a fuoco sul vetrino!!!")

N_maps = st.number_input('Numero di mappe da campionare', min_value=1, max_value=10, value=6, step=1)


with st.form(key='form'):
    ######################################
    ####### GENERAL PARAMETER  ###########
    ######################################

    st.subheader('GENERAL PARAMETERS:')


    ######################################
    paths = ['E:\\UTENTI\\Fabio Brugnara\\', 'E:\\UTENTI\\Marco Zanatta\\', 'E:\\UTENTI\\Elisa Maccadenza\\']
    folder = st.selectbox('Select folder', paths)

    spectral_range = ['1. 175-3750 cm-1 for 300 gratings, 633 laser (2193.4 cm-1)', '2. 100-2080 cm-1 for 600 gratings, 633 laser', '3. 100-1050 cm-1 for 1200 gratings, 633 laser']
    choice = st.selectbox('Select spectral range', spectral_range)

    choice=choice[0]
    if choice == '1':
        nu_min = 175
        nu_max = 3750
    elif choice == '2':
        nu_min = 100
        nu_max = 2080
    elif choice == '3':
        nu_min = 100
        nu_max = 1050


    ######################################

    t_int = st.number_input('Insert integration time [s]', min_value=0.0, max_value=50.0, value=1.0, step=0.1)
    N_int = st.number_input('Insert number of integrations', min_value=1, max_value=50, value=1, step=1)


    ######################################
    ######### FIRST MAP ##################
    ######################################

    st.subheader('MAP 1:')
    map_name = st.text_input('Insert map name', value='map1')

    st.text("Center of first map:")
    col1, col2, col3 = st.columns(3)

    X = col1.number_input('X [um]', value=0.0, step=0.1)
    Y = col2.number_input('Y [um]', value=0.0, step=0.1)
    Z = col3.number_input('Z [um]', value=0.0, step=0.1)

    if abs(Z)>500:
        st.error("ERROR: Z is too large, risk of collision")
        st.stop()

    st.text('# of points in X and Y')
    col1, col2 = st.columns(2)
    N_X = col1.number_input('N_X', value=10, step=1)
    N_Y = col2.number_input('N_Y', value=10, step=1)

      
    st.text('Distance between points in X and Y')
    col1, col2 = st.columns(2)
    D_X = col1.number_input('D_X [um]', value=100.0, step=0.1)
    D_Y = col2.number_input('D_Y [um]', value=100.0, step=0.1)


    X_min = X - (N_X-1)/2*D_X
    X_max = X + (N_X-1)/2*D_X
    Y_min = Y - (N_Y-1)/2*D_Y
    Y_max = Y + (N_Y-1)/2*D_Y


    ######################################
    ######### WRITE SCRIPT ###############
    ######################################

    with open('./template_script/'+'1st_map.txt') as f:
        lines = f.readlines()

    lines[25] = 'wMin=' + str(nu_min) + '\n'
    lines[26] = 'wMax=' + str(nu_max) + '\n'
    lines[29] = 'tSpec=' + str(t_int) + '\n'
    lines[30] = 'aSpec=' + str(N_int)  + '\n'
    lines[39] = 'MapPath = "' + folder + '"' + '\n'


    lines[46] = 'MapName = "' + map_name + '"' + '\n'
    lines[49] = "Motor1StartPosition=" + str(X_min) +   "' x-direction" + '\n'
    lines[50] = "Motor1StopPosition=" + str(X_max) + '\n'
    lines[51] = "Motor1StepSize=" + str(D_X) + '\n'
    lines[52] = "Motor2StartPosition=" + str(Y_min) + "' y-direction" + '\n'
    lines[53] = "Motor2StopPosition=" + str(Y_max) + '\n'
    lines[54] = "Motor2StepSize=" + str(D_Y) + '\n'
    lines[55] = "Motor3StopPosition=" + str(Z) + "' z-direction" + '\n'


    vec_map_name = [map_name]
    vec_X = [X]
    vec_Y = [Y]
    vec_Z = [Z]
    vec_N_X = [N_X]
    vec_N_Y = [N_Y]
    vec_D_X = [D_X]
    vec_D_Y = [D_Y]
    vec_X_min = [X_min]
    vec_X_max = [X_max]
    vec_Y_min = [Y_min]
    vec_Y_max = [Y_max]


    ######################################
    ############# NEW MAPS ###############
    ######################################

    for i in range(N_maps-1):

        st.subheader('MAP'+str(i+2)+':')
        map_name = st.text_input('Insert map name', value='map'+str(i+2))

        st.text("Center of first map:")
        col1, col2, col3 = st.columns(3)

        X = col1.number_input('X [um]', value=0.0, step=0.1, key=str(i)+'X')
        Y = col2.number_input('Y [um]', value=0.0, step=0.1, key=str(i)+'Y')
        Z = col3.number_input('Z [um]', value=0.0, step=0.1, key=str(i)+'Z')

        if abs(Z)>500:
            st.error("ERROR: Z is too large, risk of collision")
            st.stop()

        st.text('# of points in X and Y')
        col1, col2 = st.columns(2)
        N_X = col1.number_input('N_X', value=10, step=1, key=str(i)+'N_X')
        N_Y = col2.number_input('N_Y', value=10, step=1, key=str(i)+'N_Y')

        
        st.text('Distance between points in X and Y')
        col1, col2 = st.columns(2)
        D_X = col1.number_input('D_X [um]', value=100.0, step=0.1, key=str(i)+'D_X')
        D_Y = col2.number_input('D_Y [um]', value=100.0, step=0.1, key=str(i)+'D_Y')


        X_min = X - (N_X-1)/2*D_X
        X_max = X + (N_X-1)/2*D_X
        Y_min = Y - (N_Y-1)/2*D_Y
        Y_max = Y + (N_Y-1)/2*D_Y
        

        with open('./template_script/'+'Nth_map.txt') as f:
            new_lines = f.readlines()    

        new_lines[4] = 'MapName = "' + map_name + '"' + '\n'
        new_lines[7] = "Motor1StartPosition=" + str(X_min) +   "' x-direction" + '\n'
        new_lines[8] = "Motor1StopPosition=" + str(X_max) + '\n'
        new_lines[9] = "Motor1StepSize=" + str(D_X) + '\n'
        new_lines[10] = "Motor2StartPosition=" + str(Y_min) + "' y-direction \n"
        new_lines[11] = "Motor2StopPosition=" + str(Y_max) + '\n'
        new_lines[12] = "Motor2StepSize=" + str(D_Y) + '\n'
        new_lines[13] = "Motor3StopPosition=" + str(Z) + "' z-direction" + '\n'

        vec_map_name.append(map_name)
        vec_X.append(X)
        vec_Y.append(Y)
        vec_Z.append(Z)
        vec_N_X.append(N_X)
        vec_N_Y.append(N_Y)
        vec_D_X.append(D_X)
        vec_D_Y.append(D_Y)
        vec_X_min.append(X_min)
        vec_X_max.append(X_max)
        vec_Y_min.append(Y_min)
        vec_Y_max.append(Y_max)


        for i in new_lines:
            lines.append(i)

    submitted = st.form_submit_button("Submit")




########################################################
################# Ask for confirm  #####################
########################################################


vbs_script = ''
for i in lines:
    vbs_script += i

st.download_button(
    label="Download VBS script",
    data=vbs_script,
    file_name='script.vbs'
)

with st.expander("Show VBS script"):
    st.code(vbs_script, language='vbscript')