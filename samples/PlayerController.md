# Building a Physics-Based Player Controller from Scratch

This student guide breaks down how to construct a custom player controller piece by piece. Students will learn how to initialize physics components, collect hardware keyboard states, and cleanly move or rotate an object safely within Unity's physics engine.

***

## 📋 Prerequisites
Ensure your project has the following setup before beginning:
* **The Input System Package:** Installed via `Window > Package Manager` (choose *Unity Registry*, look up *Input System*, and click *Install*).
* **A Player GameObject:** A 3D Primitive capsule or cube with a **Rigidbody** component attached. Under its Rigidbody **Constraints**, check **Freeze Rotation X and Z** to keep the player standing upright.

***

## 🛠️ Step 1: Base Structure and Namespaces
When you create a blank script, it imports standard packages. To use Unity's modern input handling system, we must manually introduce its specific namespace at the top of the file.

### 📝 The Code
```csharp
using UnityEngine;
using UnityEngine.InputSystem; // Accesses modern keyboard utilities

public class PlayerController : MonoBehaviour
{
    // Variables and methods will go here
}
```

### 🔍 Explanation
* **`using UnityEngine.InputSystem;`**: Instructs the compiler to look inside the modern Input package. Without this, calling advanced hardware methods like `Keyboard.current` will trigger a compilation error.
* **`public class PlayerController : MonoBehaviour`**: Defines our script's name. This class name must match your physical file name exactly.

***

## 🛠️ Step 2: Movement Variables and Component References
Before we can calculate movements, we need configurable properties (speed and rotation speed) exposed to the Unity Editor, as well as a slot to store our hardware physics component.

### 📝 The Code
```csharp
    [Header("Movement Settings")]
    [Tooltip("Forward/back speed (units per second).")]
    public float speed = 5.0f;

    [Tooltip("Turn speed (degrees per second).")]
    public float rotationSpeed = 120.0f;

    private Rigidbody rb; // Stores reference to the physics component
```

### 🔍 Explanation
* **`public float speed` and `rotationSpeed`**: Exposing these as `public` allows students to fine-tune the variables directly inside the Unity Inspector window without opening code again.
* **`[Header]` and `[Tooltip]`**: Built-in attributes that keep the Unity Inspector organized and display helper tooltips when a user hovers their mouse over the field.
* **`private Rigidbody rb`**: A reference variable that functions as a memory container. It acts as a shortcut to hold our player's physical weight and force attributes.

***

## 🛠️ Step 3: Initializing and Caching Components
When the game starts, the script needs to locate and lock onto the physical Rigidbody component attached to the GameObject.

### 📝 The Code
```csharp
    private void Start()
    {
        // Automatically find and cache the Rigidbody component
        rb = GetComponent<Rigidbody>();
        
        // Safety check to warn the developer if the component is missing
        if (rb == null) 
        {
            Debug.LogWarning("PlayerController requires a Rigidbody component on this GameObject.");
        }
    }
```

### 🔍 Explanation
* **`Start()`**: A built-in Unity lifecycle method that fires exactly once when the scene loads up.
* **`GetComponent<Rigidbody>()`**: Queries the host GameObject for a Rigidbody. Caching this value once here saves system resources, avoiding costly component lookups later during gameplay.
* **`if (rb == null)`**: A safety net. If a student forgets to attach a Rigidbody to their player object, a bright yellow warning prints in the Unity Console to explain why physics movement isn't triggering.

***

## 🛠️ Step 4: Setting up the Physics Loop and Gathering Input
When handling physics, calculations shouldn't run on variable frame rates (`Update`). Instead, they belong in a dedicated physics loop. Within this loop, we read real-time keystrokes.

### 📝 The Code
```csharp
    private void FixedUpdate()
    {
        // Safe exit if the Rigidbody wasn't found
        if (rb == null) return;

        // Container to hold current button directions
        Vector2 moveInput = Vector2.zero;

        // 1. Check Forward/Backward (Y-axis)
        if (Keyboard.current.wKey.isPressed || Keyboard.current.upArrowKey.isPressed) 
            moveInput.y = 1f;
        if (Keyboard.current.sKey.isPressed || Keyboard.current.downArrowKey.isPressed) 
            moveInput.y = -1f;

        // 2. Check Left/Right Turning (X-axis)
        if (Keyboard.current.dKey.isPressed || Keyboard.current.rightArrowKey.isPressed) 
            moveInput.x = 1f;
        if (Keyboard.current.aKey.isPressed || Keyboard.current.leftArrowKey.isPressed) 
            moveInput.x = -1f;
            
        // Physical calculations will be appended right below this line
    }
```

### 🔍 Explanation
* **`FixedUpdate()`**: Unlike `Update()`, this runs on a strict, constant timer (defaulting to 50 ticks per second). This ensures physics behavior behaves identically on a cheap low-end laptop and an expensive high-end gaming PC.
* **`Keyboard.current.xKey.isPressed`**: Explicitly reads the immediate physical hardware state of the keyboard. If the key is being held down, it evaluates to `true`.
* **`moveInput.y` and `moveInput.x`**: Compiles separate hardware keys into a uniform coordinate direction system. Pressing **W** gives a value of `1` (positive vertical), while pressing **S** yields `-1` (negative vertical).

***

## 🛠️ Step 5: Applying Turning and Rotation Physics
Rather than snapping an object's rotation instantly, we calculate a precise fractional rotation offset based on time and push the object safely via the physics solver.

### 📝 The Code
```csharp
        // Append this into your FixedUpdate below the input checks:

        // 3. Process Turning
        float turn = moveInput.x * rotationSpeed * Time.fixedDeltaTime;
        Quaternion turnRotation = Quaternion.Euler(0f, turn, 0f);
        rb.MoveRotation(rb.rotation * turnRotation);
```

### 🔍 Explanation
* **`Time.fixedDeltaTime`**: Represents the fraction of time elapsed between physics ticks. Multiplying by this ensures that your `rotationSpeed` scales correctly over real time (meaning 120 degrees per *second*, not per frame).
* **`Quaternion.Euler(0f, turn, 0f)`**: Computes structural angles. Since we want our player to spin left and right on a flat plane like a top, we only manipulate the **Y-axis**.
* **`rb.MoveRotation()`**: Tell the engine to sweep the object cleanly into its new rotation angle. This naturally respects wall collisions along the way instead of forcing a teleportation bug.

***

## 🛠️ Step 6: Applying Directional Forward and Backward Movement
Finally, we calculate movement. The player must move relative to the exact direction they are currently facing, not global grid coordinates.

### 📝 The Code
```csharp
        // Append this at the very bottom of your FixedUpdate:

        // 4. Process Forward/Backward Movement
        Vector3 movement = transform.forward * moveInput.y * speed * Time.fixedDeltaTime;
        rb.MovePosition(rb.position + movement);
```

### 🔍 Explanation
* **`transform.forward`**: A directional vector that indicates the object's personal "front" side. Multiplying by this ensures that if a player spins 90 degrees to face left, pressing **W** drives them in their new forward direction.
* **`rb.MovePosition(rb.position + movement)`**: Takes the player's exact current physical position (`rb.position`), shifts it slightly by our computed `movement` offset, and physically slides the object to its destination.

***

## 🏁 The Complete Composite Script
When all elements are combined sequentially, your students' final script should look like this:

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    [Header("Movement Settings")]
    [Tooltip("Forward/back speed (units per second).")]
    public float speed = 5.0f;

    [Tooltip("Turn speed (degrees per second).")]
    public float rotationSpeed = 120.0f;

    private Rigidbody rb;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        if (rb == null) 
        {
            Debug.LogWarning("PlayerController requires a Rigidbody component on this GameObject.");
        }
    }

    private void FixedUpdate()
    {
        if (rb == null) return;

        Vector2 moveInput = Vector2.zero;

        if (Keyboard.current.wKey.isPressed || Keyboard.current.upArrowKey.isPressed) 
            moveInput.y = 1f;
        if (Keyboard.current.sKey.isPressed || Keyboard.current.downArrowKey.isPressed) 
            moveInput.y = -1f;

        if (Keyboard.current.dKey.isPressed || Keyboard.current.rightArrowKey.isPressed) 
            moveInput.x = 1f;
        if (Keyboard.current.aKey.isPressed || Keyboard.current.leftArrowKey.isPressed) 
            moveInput.x = -1f;

        float turn = moveInput.x * rotationSpeed * Time.fixedDeltaTime;
        Quaternion turnRotation = Quaternion.Euler(0f, turn, 0f);
        rb.MoveRotation(rb.rotation * turnRotation);

        Vector3 movement = transform.forward * moveInput.y * speed * Time.fixedDeltaTime;
        rb.MovePosition(rb.position + movement);
    }
}
```
