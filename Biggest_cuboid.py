import csv

# Brick sizes
BRICK_L = 200  # mm
BRICK_W = 100  # mm
BRICK_H = 100  # mm

def find_largest_cuboid(max_bricks=10000, brick_volume=200*100*100, thickness=200, step=200):
    best = (0, 0, 0, 0, 0) # (Total Bricks, L, W, H, Wall Volume)
    
    limit = 10000

    for L in range(2 * thickness, limit + 1, step):
        for W in range(2 * thickness, limit + 1, step):
            for H in range(2 * thickness, limit + 1, step):
                outer_volume = L * W * H
                inner_volume = (L - 2 * thickness) * (W - 2 * thickness) * (H - 2 * thickness)
                wall_volume = outer_volume - inner_volume
                
                if wall_volume % brick_volume == 0:
                    bricks_needed = wall_volume // brick_volume
                    
                    if bricks_needed <= max_bricks:
                        if bricks_needed > best[0]:
                            best = (bricks_needed, L, W, H, wall_volume)
                            
    return best

def generate_cuboid(L, W, H, thickness, filename="bricks_layout.csv"):
    """
    Generates a CSV file with the location and orientation of every brick
    in a hollow cuboid by building each of the six faces.
    """
    bricks = []

    # 1. Bottom Face (at z=0) and Top Face (at z=H-thickness)
    for z in [0, H - thickness]:
        for x in range(0, L, BRICK_L):
            for y in range(0, W, BRICK_W):
                bricks.append([x, y, z, "XY", BRICK_L, BRICK_W, BRICK_H])

    # 2. Front Face (at y=0) and Back Face (at y=W-thickness)
    for y in [0, W - thickness]:
        for x in range(0, L, BRICK_L):
            for z in range(thickness, H - thickness, BRICK_H):
                bricks.append([x, y, z, "XZ", BRICK_L, BRICK_W, BRICK_H])

    # 3. Left Face (at x=0) and Right Face (at x=L-thickness)
    for x in [0, L - thickness]:
        for y in range(thickness, W - thickness, BRICK_W):
            for z in range(thickness, H - thickness, BRICK_H):
                bricks.append([x, y, z, "YZ", BRICK_W, BRICK_L, BRICK_H])
    
    # Remove duplicates from corners where walls overlap
    unique_bricks = [list(x) for x in set(tuple(x) for x in bricks)]

    # Save CSV
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z", "orientation", "length", "width", "height"])
        writer.writerows(unique_bricks)

    print(f"Bricks layout saved: {filename}")
    print(f"Total bricks: {len(unique_bricks)}")

if __name__ == "__main__":
    bricks, L, W, H, wall_volume = find_largest_cuboid(max_bricks=10000)
    
    print(f"Largest Cuboid Dimensions (mm): L={L}, W={W}, H={H}")
    print(f"Outer Volume: {L*W*H:,} mm³")
    print(f"Wall Volume: {wall_volume:,} mm³")
    print(f"Number of Bricks: {bricks:,}")
    print(f"Hollow Volume: {(L*W*H)-wall_volume:,} mm³")

    # Generate the brick layout for this cuboid
    generate_cuboid(L, W, H, 200)