def find_largest_cuboid(max_bricks=10000, brick_volume=200*100*100, thickness=200, step=100):
    total_volume = max_bricks * brick_volume
    best = (0, 0, 0, 0)  # (Volume, L, W, H, Wall_Volume)

    # We need to search dimensions in multiples of 100
    # Let's limit L, W, H up to a reasonable bound (e.g., 10000 mm)
    limit = 10000

    for L in range(2*thickness, limit+1, step):
        for W in range(2*thickness, limit+1, step):
            for H in range(2*thickness, limit+1, step):
                outer = L * W * H
                inner = (L - 2*thickness) * (W - 2*thickness) * (H - 2*thickness)
                wall_volume = outer - inner

                if wall_volume <= total_volume:
                    if outer > best[0]:  # maximize outer cuboid volume
                        best = (outer, L, W, H, wall_volume)

    return best


if __name__ == "__main__":
    volume, L, W, H, wall_volume = find_largest_cuboid()
    print(f"Largest Cuboid Dimensions (mm): L={L}, W={W}, H={H}")
    print(f"Outer Volume: {volume:,} mm³")
    print(f"Wall Volume: {wall_volume:,} mm³ (<= {10_000*200*100*100:,})")
    print(f"Hollow Volume: {volume-wall_volume} mm³")

import csv

# Brick sizes
BRICK_L = 200  # mm
BRICK_W = 100  # mm
BRICK_H = 100  # mm

# Largest cuboid under half-brick rule (from your result)
L, W, H = 4200, 4300, 4300
WALL = 200  # mm

def place_wall(start_x, start_y, start_z, dim_x, dim_y, orientation, bricks):
    """
    Place a wall made of bricks, allowing half-bricks at edges.
    """
    if orientation == "X":  # Wall along X direction
        step = BRICK_L
        ysize = BRICK_W
        zsize = BRICK_H
        for x in range(0, dim_x, BRICK_L):
            length = BRICK_L if x + BRICK_L <= dim_x else dim_x - x
            bricks.append([start_x + x, start_y, start_z, "X", length, ysize, zsize])
    elif orientation == "Y":  # Wall along Y direction
        step = BRICK_L
        xsize = BRICK_W
        zsize = BRICK_H
        for y in range(0, dim_y, BRICK_L):
            length = BRICK_L if y + BRICK_L <= dim_y else dim_y - y
            bricks.append([start_x, start_y + y, start_z, "Y", xsize, length, zsize])
    elif orientation == "Z":  # Wall along Z (vertical)
        step = BRICK_H
        xsize = BRICK_L
        ysize = BRICK_W
        for z in range(0, dim_y, BRICK_H):
            height = BRICK_H if z + BRICK_H <= dim_y else dim_y - z
            bricks.append([start_x, start_y, start_z + z, "Z", xsize, ysize, height])

def generate_cuboid(L, W, H, thickness, filename="bricks_layout.csv"):

    bricks = []
    
    # Calculate wall dimensions
    inner_L = L - 2 * thickness
    inner_W = W - 2 * thickness
    
    # 1. Bottom and Top Walls (Floor and Ceiling)
    for z in [0, H - thickness]:
        for x in range(0, L, BRICK_L):
            for y in range(0, W, BRICK_W):
                bricks.append([x, y, z, "Z", BRICK_L, BRICK_W, BRICK_H])

    # 2. Side Walls (Front, Back, Left, Right)
    # Front and Back Walls
    for y in [0, W - thickness]:
        for x in range(0, L, BRICK_L):
            for z in range(thickness, H - thickness, BRICK_H):
                bricks.append([x, y, z, "X", BRICK_L, BRICK_W, BRICK_H])

    # Left and Right Walls
    for x in [0, L - thickness]:
        for y in range(thickness, W - thickness, BRICK_W):
            for z in range(thickness, H - thickness, BRICK_H):
                bricks.append([x, y, z, "Y", BRICK_L, BRICK_W, BRICK_H])

    # Remove duplicates from corners where walls overlap
    unique_bricks = [list(x) for x in set(tuple(x) for x in bricks)]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z", "orientation", "length", "width", "height"])
        writer.writerows(unique_bricks)

    print(f"Bricks layout saved: {filename}")
    print(f"Total bricks (deduplicated): {len(unique_bricks)}")

L, W, H = 4200, 4300, 4300
WALL_THICKNESS = 200 

# Run the corrected function
generate_cuboid(L, W, H, WALL_THICKNESS)