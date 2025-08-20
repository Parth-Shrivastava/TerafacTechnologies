def find_largest_cuboid(max_bricks=10000, brick_volume=200*100*100, thickness=200, step=200):
    total_volume = max_bricks * brick_volume
    best = (0, 0, 0, 0, 0)  # (Volume, L, W, H, Wall_Volume)
    limit = 10000

    for L in range(2 * thickness, limit + 1, step):
        for W in range(2 * thickness, limit + 1, step):
            for H in range(2 * thickness, limit + 1, step):
                outer = L * W * H
                inner = (L - 2 * thickness) * (W - 2 * thickness) * (H - 2 * thickness)
                wall_volume = outer - inner

                if wall_volume <= total_volume:
                    if outer > best[0]:
                        best = (outer, L, W, H, wall_volume)

    return best

if __name__ == "__main__":
    volume, L, W, H, wall_volume = find_largest_cuboid()
    print(f"Largest Cuboid Dimensions (mm): L={L}, W={W}, H={H}")
    print(f"Outer Volume: {volume:,} mm³")
    print(f"Wall Volume: {wall_volume:,} mm³")
    print(f"Number of Bricks: {wall_volume // (200 * 100 * 100):,}")
    print(f"Hollow Volume: {volume - wall_volume:,} mm³")

# import csv

# Brick sizes
# BRICK_L = 200  # mm
# BRICK_W = 100  # mm
# BRICK_H = 100  # mm

# Largest cuboid under half-brick rule (from your result)
# L, W, H = 4200, 4300, 4300
# WALL = 200  # mm


import csv

# Brick sizes
BRICK_L = 200  # mm
BRICK_W = 100  # mm
BRICK_H = 100  # mm

def generate_cuboid(L, W, H, thickness, filename="bricks_layout.csv"):
    """
    Generates a CSV file with the location and orientation of every brick
    in a hollow cuboid by building each of the six faces.
    """
    bricks = []
    
    # 1. Bottom Face (at z=0)
    # The bottom wall has dimensions L x W x thickness.
    # Bricks are laid flat, using their L x W dimensions for x,y coordinates.
    num_bricks_bottom = (L // BRICK_L) * (W // BRICK_W)
    for i in range(num_bricks_bottom):
        x = (i % (L // BRICK_L)) * BRICK_L
        y = (i // (L // BRICK_L)) * BRICK_W
        bricks.append([x, y, 0, "XY", BRICK_L, BRICK_W, BRICK_H])

    # 2. Top Face (at z=H-thickness)
    # The top wall also has dimensions L x W x thickness.
    # Bricks are laid flat.
    for i in range(num_bricks_bottom):
        x = (i % (L // BRICK_L)) * BRICK_L
        y = (i // (L // BRICK_L)) * BRICK_W
        bricks.append([x, y, H - thickness, "XY", BRICK_L, BRICK_W, BRICK_H])
            
    # 3. Front and Back Faces
    # These walls span length L and height (H - 2*thickness).
    # Bricks are placed vertically.
    num_bricks_front_back = (L // BRICK_L) * ((H - 2*thickness) // BRICK_H)
    for i in range(num_bricks_front_back):
        x = (i % (L // BRICK_L)) * BRICK_L
        z = thickness + (i // (L // BRICK_L)) * BRICK_H
        # Front wall (at y=0)
        bricks.append([x, 0, z, "XZ", BRICK_L, BRICK_W, BRICK_H])
        # Back wall (at y=W-thickness)
        bricks.append([x, W - thickness, z, "XZ", BRICK_L, BRICK_W, BRICK_H])
            
    # 4. Left and Right Faces
    # These walls span the inner width (W-2*thickness) and height (H-2*thickness).
    # Bricks are placed vertically, rotated 90 degrees.
    num_bricks_left_right = ((W - 2*thickness) // BRICK_W) * ((H - 2*thickness) // BRICK_H)
    for i in range(num_bricks_left_right):
        y = thickness + (i % ((W - 2*thickness) // BRICK_W)) * BRICK_W
        z = thickness + (i // ((W - 2*thickness) // BRICK_W)) * BRICK_H
        # Left wall (at x=0)
        bricks.append([0, y, z, "YZ", BRICK_W, BRICK_L, BRICK_H])
        # Right wall (at x=L-thickness)
        bricks.append([L - thickness, y, z, "YZ", BRICK_W, BRICK_L, BRICK_H])

    # Save CSV
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z", "orientation", "length", "width", "height"])
        writer.writerows(bricks)

    print(f"Bricks layout saved: {filename}")
    print(f"Total bricks: {len(bricks)}")

if __name__ == "__main__":
    # Use the dimensions from the 'find_largest_cuboid' function in the previous corrected code
    L, W, H = 4200, 4200, 4400
    WALL_THICKNESS = 200
    
    # Run the corrected function to generate the brick layout
    generate_cuboid(L, W, H, WALL_THICKNESS)