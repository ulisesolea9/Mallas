input_file = '/home/ulises/Mallasmesh_ONERAM6_inv_ffd.su2'

# Leer y mostrar las primeras líneas del archivo SU2 para inspección
def preview_su2_file(file_path, num_lines=10):
    with open(file_path, 'r') as file:
        for _ in range(num_lines):
            print(file.readline().strip())

# Mostrar las primeras líneas del archivo
preview_su2_file(input_file)
