# Creating a Physics-Based Character Controller

This student guide provides a complete workflow for implementing custom keyboard controls in Unity using the Input System package and Rigidbody physics.

## Prerequisites

Before you begin, ensure your project is properly configured:

1. Install the Input System:
   - Navigate to `Window > Package Manager`.
   - Set the dropdown to **Packages: Unity Registry**.
   - Locate **Input System and click Install**.
   - Let Unity restart to activate the backend if prompted.
2. Setup Your Game Object:
   - Create a 3D Primitive (e.g., a Capsule or Cube) to represent your Player.
   - Add a **Rigidbody** component via the Inspector window.
   - Under the Rigidbody's Constraints, freeze the X and Z rotations so your player doesn't tip over.
