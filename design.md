# Design Document: Rupant AI - AI-Powered Lab Simulator

## Overview

Rupant AI is a comprehensive virtual laboratory platform designed to democratize science education for rural Indian schools. The system combines multilingual AI tutoring, realistic experiment simulations, and safety training in a low-bandwidth-optimized web application.

### Core Design Principles

1. **Accessibility First**: Optimized for low-bandwidth connections and basic hardware
2. **Multilingual by Design**: Native support for 6 Indian languages plus English
3. **Offline-Capable**: Core functionality works without continuous internet connectivity
4. **Pedagogically Sound**: Aligned with CBSE curriculum and learning science principles
5. **Scalable Architecture**: Serverless design handles varying load efficiently

### Technology Stack

- **Frontend**: Python with Streamlit framework for rapid web UI development
- **Backend**: Python with AWS Lambda for serverless compute
- **AI Services**: Amazon Bedrock for multilingual conversational AI
- **Voice Services**: Amazon Polly for text-to-speech in multiple languages
- **Data Storage**: Amazon DynamoDB for user data and progress tracking
- **Asset Storage**: Amazon S3 for experiment assets and media
- **API Gateway**: AWS API Gateway for RESTful endpoints
- **Authentication**: AWS Cognito for user management

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Student Browser                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Streamlit Frontend (Python)                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │ │
│  │  │ AI Tutor │  │ Virtual  │  │  Safety Simulator    │ │ │
│  │  │   UI     │  │  Lab UI  │  │       UI             │ │ │
│  │  └──────────┘  └──────────┘  └──────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │     Local Storage / IndexedDB (Offline Cache)    │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS / REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS API Gateway                           │
│              (RESTful API Endpoints)                         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Lambda:    │   │   Lambda:    │   │   Lambda:    │
│  AI Tutor    │   │ Virtual Lab  │   │   Safety     │
│   Service    │   │   Service    │   │   Service    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Amazon     │   │   Amazon     │   │  DynamoDB    │
│   Bedrock    │   │    Polly     │   │  (User Data) │
│  (AI Model)  │   │   (Voice)    │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
                                              │
                                              ▼
                                      ┌──────────────┐
                                      │  Amazon S3   │
                                      │   (Assets)   │
                                      └──────────────┘
```

## Architecture

### Frontend Architecture (Streamlit + Python)

The frontend is built using Streamlit, a Python framework that enables rapid development of interactive web applications. This choice aligns with the Python-based tech stack and simplifies deployment.

**Key Components:**

1. **Main Application (`app.py`)**
   - Entry point for the Streamlit application
   - Handles routing between different views (AI Tutor, Virtual Lab, Safety Simulator)
   - Manages session state and user authentication
   - Implements offline detection and graceful degradation

2. **AI Tutor Interface (`components/ai_tutor.py`)**
   - Chat interface for student-AI interactions
   - Language selector with persistence
   - Voice output controls
   - Context-aware help during experiments

3. **Virtual Lab Interface (`components/virtual_lab.py`)**
   - Experiment selection and browsing
   - Interactive experiment canvas using Streamlit components
   - Real-time simulation visualization
   - Measurement tools and controls

4. **Safety Simulator Interface (`components/safety_simulator.py`)**
   - Scenario presentation and interaction
   - Decision-making interface
   - Feedback and explanation display
   - Certification tracking

5. **Offline Manager (`utils/offline_manager.py`)**
   - Detects connectivity status
   - Manages local storage using browser APIs
   - Queues operations for sync when online
   - Caches experiment definitions and assets

6. **State Manager (`utils/state_manager.py`)**
   - Centralized session state management
   - Experiment state persistence
   - User progress tracking
   - Language context management

### Backend Architecture (AWS Lambda + Python)

The backend uses AWS Lambda functions written in Python, providing serverless scalability and cost-efficiency.

**Lambda Functions:**

1. **AI Tutor Service (`lambda/ai_tutor_service.py`)**
   - Handles chat requests from students
   - Integrates with Amazon Bedrock for AI responses
   - Manages conversation context and history
   - Implements language-specific prompt engineering
   - Provides context-aware assistance during experiments

2. **Virtual Lab Service (`lambda/virtual_lab_service.py`)**
   - Manages experiment lifecycle (start, update, complete)
   - Executes simulation logic
   - Validates student actions
   - Generates lab reports
   - Tracks experiment progress

3. **Safety Service (`lambda/safety_service.py`)**
   - Manages safety scenarios
   - Evaluates student decisions
   - Provides feedback and explanations
   - Issues safety certifications
   - Enforces prerequisites for advanced experiments

4. **User Service (`lambda/user_service.py`)**
   - Handles user authentication and authorization
   - Manages user profiles and preferences
   - Tracks progress and achievements
   - Generates progress reports

5. **Content Service (`lambda/content_service.py`)**
   - Serves experiment definitions
   - Manages experiment library and metadata
   - Handles search and filtering
   - Provides recommendations

6. **Voice Service (`lambda/voice_service.py`)**
   - Integrates with Amazon Polly
   - Converts text to speech in selected language
   - Manages voice settings (rate, volume)
   - Caches frequently used audio

### Data Architecture

**DynamoDB Tables:**

1. **Users Table**
   - Partition Key: `user_id`
   - Attributes: profile, preferences, language, progress_summary
   - GSI: `email-index` for login

2. **Experiments Table**
   - Partition Key: `experiment_id`
   - Attributes: title, description, subject, grade_level, difficulty, definition, assets
   - GSI: `subject-grade-index` for filtering

3. **UserProgress Table**
   - Partition Key: `user_id`
   - Sort Key: `experiment_id`
   - Attributes: status, score, attempts, completion_date, lab_report

4. **SafetyCertifications Table**
   - Partition Key: `user_id`
   - Sort Key: `certification_type`
   - Attributes: earned_date, scenario_scores

5. **ConversationHistory Table**
   - Partition Key: `user_id`
   - Sort Key: `timestamp`
   - Attributes: message, response, language, experiment_context
   - TTL: 30 days (for cost management)

6. **ExperimentSessions Table**
   - Partition Key: `session_id`
   - Attributes: user_id, experiment_id, state, started_at, last_updated
   - TTL: 7 days (cleanup abandoned sessions)

**S3 Buckets:**

1. **Experiment Assets Bucket**
   - Images, videos, 3D models for experiments
   - Organized by experiment_id
   - CloudFront CDN for fast delivery

2. **User Generated Content Bucket**
   - Lab reports, certificates
   - Organized by user_id
   - Lifecycle policy for archival

## Components and Interfaces

### 1. AI Tutor Component

**Purpose**: Provides multilingual conversational AI assistance to students.

**Key Classes:**

```python
class AITutor:
    """Main AI tutor interface"""
    
    def __init__(self, bedrock_client, language: str):
        self.bedrock_client = bedrock_client
        self.language = language
        self.conversation_history = []
    
    def ask_question(self, question: str, experiment_context: dict = None) -> str:
        """
        Process student question and return AI response
        
        Args:
            question: Student's question in selected language
            experiment_context: Current experiment state if applicable
            
        Returns:
            AI response in same language
        """
        pass
    
    def switch_language(self, new_language: str) -> None:
        """Switch conversation language while preserving context"""
        pass
    
    def get_contextual_hint(self, experiment_state: dict) -> str:
        """Generate proactive hint based on experiment progress"""
        pass

class BedrockIntegration:
    """Integration with Amazon Bedrock for AI capabilities"""
    
    def __init__(self, model_id: str = "anthropic.claude-v2"):
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime')
    
    def generate_response(self, prompt: str, language: str, 
                         conversation_history: list) -> str:
        """Generate AI response using Bedrock"""
        pass
    
    def build_prompt(self, question: str, language: str, 
                    experiment_context: dict = None) -> str:
        """Build language-specific prompt with context"""
        pass
```

**API Endpoints:**

- `POST /api/ai-tutor/ask` - Submit question to AI tutor
- `POST /api/ai-tutor/switch-language` - Change conversation language
- `GET /api/ai-tutor/history` - Retrieve conversation history

### 2. Virtual Lab Component

**Purpose**: Simulates scientific experiments with realistic physics, chemistry, and biology models.

**Key Classes:**

```python
class VirtualLab:
    """Main virtual lab controller"""
    
    def __init__(self, experiment_id: str):
        self.experiment_id = experiment_id
        self.experiment_def = None
        self.state = ExperimentState()
        self.simulator = None
    
    def start_experiment(self) -> ExperimentState:
        """Initialize experiment with equipment and materials"""
        pass
    
    def perform_action(self, action: Action) -> ActionResult:
        """Execute student action and update state"""
        pass
    
    def get_measurement(self, tool: str, target: str) -> Measurement:
        """Use measurement tool on target object"""
        pass
    
    def undo_last_action(self) -> ExperimentState:
        """Revert to previous state"""
        pass
    
    def complete_experiment(self) -> LabReport:
        """Finalize experiment and generate report"""
        pass

class ExperimentState:
    """Represents current state of an experiment"""
    
    def __init__(self):
        self.equipment: Dict[str, Equipment] = {}
        self.materials: Dict[str, Material] = {}
        self.measurements: List[Measurement] = []
        self.actions_history: List[Action] = []
        self.observations: List[str] = []
    
    def to_dict(self) -> dict:
        """Serialize state for storage/transmission"""
        pass
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ExperimentState':
        """Deserialize state from storage"""
        pass

class SimulationEngine:
    """Base class for physics/chemistry/biology simulations"""
    
    def simulate_action(self, action: Action, state: ExperimentState) -> ExperimentState:
        """Apply physics/chemistry rules to update state"""
        pass
    
    def validate_action(self, action: Action, state: ExperimentState) -> ValidationResult:
        """Check if action is physically possible"""
        pass

class PhysicsSimulator(SimulationEngine):
    """Simulates physics experiments (circuits, mechanics, optics)"""
    
    def calculate_circuit_values(self, circuit: Circuit) -> dict:
        """Apply Ohm's law and Kirchhoff's rules"""
        pass
    
    def simulate_motion(self, object: PhysicsObject, forces: List[Force], 
                       time_delta: float) -> PhysicsObject:
        """Apply Newton's laws to update object state"""
        pass

class ChemistrySimulator(SimulationEngine):
    """Simulates chemistry experiments (reactions, titrations)"""
    
    def simulate_reaction(self, reactants: List[Chemical], 
                         conditions: dict) -> List[Chemical]:
        """Apply stoichiometry and reaction kinetics"""
        pass
    
    def calculate_ph(self, solution: Solution) -> float:
        """Calculate pH based on concentration"""
        pass

class BiologySimulator(SimulationEngine):
    """Simulates biology experiments (microscopy, dissection)"""
    
    def simulate_cell_observation(self, specimen: Specimen, 
                                  magnification: int) -> Image:
        """Generate microscope view"""
        pass
```

**API Endpoints:**

- `POST /api/lab/start` - Start new experiment session
- `POST /api/lab/action` - Perform action in experiment
- `GET /api/lab/state` - Get current experiment state
- `POST /api/lab/measure` - Use measurement tool
- `POST /api/lab/undo` - Undo last action
- `POST /api/lab/complete` - Complete experiment and get report

### 3. Safety Simulator Component

**Purpose**: Teaches lab safety through interactive scenarios.

**Key Classes:**

```python
class SafetySimulator:
    """Manages safety training scenarios"""
    
    def __init__(self):
        self.scenarios = self.load_scenarios()
    
    def get_scenario(self, scenario_type: str) -> SafetyScenario:
        """Load a safety scenario"""
        pass
    
    def evaluate_decision(self, scenario_id: str, decision: str) -> Evaluation:
        """Evaluate student's safety decision"""
        pass
    
    def issue_certification(self, user_id: str, 
                           certification_type: str) -> Certificate:
        """Issue safety certification after successful completion"""
        pass
    
    def check_prerequisites(self, user_id: str, 
                           experiment_id: str) -> bool:
        """Verify user has required safety training"""
        pass

class SafetyScenario:
    """Represents a safety training scenario"""
    
    def __init__(self, scenario_id: str, hazard_type: str):
        self.scenario_id = scenario_id
        self.hazard_type = hazard_type  # chemical, electrical, fire, biological
        self.description = ""
        self.choices: List[Choice] = []
        self.correct_choice_id = ""
        self.explanations: Dict[str, str] = {}

class SafetyMonitor:
    """Monitors experiments for safety violations"""
    
    def check_action_safety(self, action: Action, 
                           state: ExperimentState) -> SafetyCheck:
        """Verify action doesn't violate safety rules"""
        pass
    
    def pause_for_violation(self, violation: SafetyViolation) -> Guidance:
        """Pause experiment and provide corrective guidance"""
        pass
```

**API Endpoints:**

- `GET /api/safety/scenarios` - List available safety scenarios
- `GET /api/safety/scenario/{id}` - Get specific scenario
- `POST /api/safety/evaluate` - Evaluate student decision
- `GET /api/safety/certifications/{user_id}` - Get user certifications
- `POST /api/safety/check-prerequisites` - Verify safety training

### 4. Voice Synthesis Component

**Purpose**: Converts text to speech in multiple Indian languages.

**Key Classes:**

```python
class VoiceSynthesizer:
    """Integration with Amazon Polly for text-to-speech"""
    
    def __init__(self):
        self.polly_client = boto3.client('polly')
        self.voice_map = {
            'hindi': 'Aditi',
            'tamil': 'Aditi',  # Polly supports limited Indian languages
            'english': 'Raveena',
            # Map languages to available Polly voices
        }
    
    def synthesize_speech(self, text: str, language: str, 
                         rate: str = 'medium', 
                         volume: str = 'medium') -> bytes:
        """Convert text to speech audio"""
        pass
    
    def get_audio_url(self, text: str, language: str) -> str:
        """Generate and return S3 URL for audio"""
        pass
    
    def cache_audio(self, text: str, language: str, audio_data: bytes) -> str:
        """Cache frequently used audio in S3"""
        pass
```

**API Endpoints:**

- `POST /api/voice/synthesize` - Convert text to speech
- `GET /api/voice/audio/{audio_id}` - Retrieve cached audio

### 5. Offline Manager Component

**Purpose**: Enables offline functionality and data synchronization.

**Key Classes:**

```python
class OfflineManager:
    """Manages offline capabilities and sync"""
    
    def __init__(self):
        self.is_online = True
        self.pending_operations = []
        self.cached_experiments = {}
    
    def detect_connectivity(self) -> bool:
        """Check internet connectivity status"""
        pass
    
    def cache_experiment(self, experiment_id: str, 
                        experiment_data: dict) -> None:
        """Store experiment definition locally"""
        pass
    
    def save_state_locally(self, state: ExperimentState) -> None:
        """Persist experiment state to browser storage"""
        pass
    
    def queue_operation(self, operation: Operation) -> None:
        """Queue operation for sync when online"""
        pass
    
    def sync_when_online(self) -> SyncResult:
        """Synchronize pending operations with backend"""
        pass
    
    def load_cached_experiment(self, experiment_id: str) -> dict:
        """Load experiment from local cache"""
        pass
```

## Data Models

### Core Data Structures

```python
@dataclass
class User:
    user_id: str
    email: str
    name: str
    preferred_language: str
    grade_level: int
    school_id: str
    created_at: datetime
    last_login: datetime

@dataclass
class Experiment:
    experiment_id: str
    title: Dict[str, str]  # Multilingual titles
    description: Dict[str, str]  # Multilingual descriptions
    subject: str  # physics, chemistry, biology
    grade_level: int
    difficulty: str  # beginner, intermediate, advanced
    estimated_duration: int  # minutes
    learning_objectives: List[str]
    safety_requirements: List[str]
    equipment_list: List[str]
    procedure_steps: List[Dict]
    simulation_config: dict
    assets: Dict[str, str]  # asset_type -> S3 URL

@dataclass
class Action:
    action_type: str  # move, mix, heat, measure, connect, etc.
    target: str  # object being acted upon
    parameters: dict  # action-specific parameters
    timestamp: datetime

@dataclass
class Measurement:
    tool: str  # thermometer, ruler, pH_meter, multimeter
    target: str  # what was measured
    value: float
    unit: str
    uncertainty: float
    timestamp: datetime

@dataclass
class LabReport:
    experiment_id: str
    user_id: str
    title: str
    objective: str
    materials_used: List[str]
    procedure: List[str]
    observations: List[str]
    measurements: List[Measurement]
    results: str
    analysis: str
    conclusion: str
    generated_at: datetime

@dataclass
class UserProgress:
    user_id: str
    experiment_id: str
    status: str  # not_started, in_progress, completed
    score: float
    attempts: int
    completion_date: Optional[datetime]
    lab_report_url: Optional[str]
    time_spent: int  # minutes

@dataclass
class SafetyCertification:
    user_id: str
    certification_type: str  # chemical, electrical, fire, biological
    earned_date: datetime
    scenario_scores: Dict[str, float]
    expiry_date: Optional[datetime]

@dataclass
class ConversationMessage:
    user_id: str
    message: str
    response: str
    language: str
    experiment_context: Optional[dict]
    timestamp: datetime
```

### Experiment Definition Schema

Experiments are defined using JSON/YAML configuration files:

```python
experiment_schema = {
    "experiment_id": "string",
    "metadata": {
        "title": {"en": "...", "hi": "...", "ta": "..."},
        "description": {"en": "...", "hi": "...", "ta": "..."},
        "subject": "physics|chemistry|biology",
        "grade_level": "int",
        "difficulty": "beginner|intermediate|advanced",
        "duration_minutes": "int",
        "learning_objectives": ["string"],
        "safety_requirements": ["string"]
    },
    "equipment": [
        {
            "id": "string",
            "name": {"en": "...", "hi": "..."},
            "type": "string",
            "initial_state": {}
        }
    ],
    "materials": [
        {
            "id": "string",
            "name": {"en": "...", "hi": "..."},
            "quantity": "float",
            "unit": "string",
            "properties": {}
        }
    ],
    "simulation": {
        "type": "physics|chemistry|biology",
        "engine": "string",
        "rules": {},
        "constraints": {}
    },
    "procedure": [
        {
            "step": "int",
            "instruction": {"en": "...", "hi": "..."},
            "expected_actions": ["string"],
            "safety_notes": ["string"]
        }
    ],
    "assessment": {
        "scoring_criteria": {},
        "required_measurements": ["string"],
        "expected_results": {}
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I've identified the following testable properties and eliminated redundancies:

**Redundancies Identified:**
- Requirements 2.5 and 5.6 both test measurement output format - combined into Property 8
- Requirements 10.2 and 10.6 both test data persistence - combined into Property 18
- Requirements 11.3 and 11.5 both test accessibility attributes - combined into Property 20

**Properties to Implement:**

### Property 1: Language Context Persistence
*For any* language selection and any sequence of interactions within a session, the system's Language_Context should remain consistent with the selected language.

**Validates: Requirements 1.2**

### Property 2: Language Switch Context Preservation
*For any* active session with conversation history, switching languages should preserve all conversation context while changing only the output language.

**Validates: Requirements 1.6**

### Property 3: Experiment Initialization Completeness
*For any* experiment definition, starting the experiment should create an ExperimentState containing all equipment and materials specified in the experiment definition.

**Validates: Requirements 2.2**

### Property 4: State Update Consistency
*For any* valid action performed in the Virtual_Lab, the ExperimentState should be updated to reflect the action's effects according to simulation rules.

**Validates: Requirements 2.3**

### Property 5: Physical Law Conservation
*For any* physics simulation, the system should enforce conservation of mass, energy, and charge throughout all state transitions.

**Validates: Requirements 2.4, 13.5**

### Property 6: Lab Report Generation Completeness
*For any* completed experiment, the generated LabReport should contain all required sections: objective, materials, procedure, observations, measurements, results, analysis, and conclusion.

**Validates: Requirements 2.7**

### Property 7: Safety Decision Evaluation
*For any* unsafe choice made in a SafetyScenario, the system should provide an explanation of consequences and the correct procedure.

**Validates: Requirements 3.2**

### Property 8: Measurement Output Format
*For any* measurement taken using any measurement tool, the output should include the numeric value, appropriate unit, and precision level.

**Validates: Requirements 2.5, 5.6**

### Property 9: Safety Certification Issuance
*For any* correctly completed SafetyScenario, the system should issue a SafetyCertification and provide positive reinforcement.

**Validates: Requirements 3.4**

### Property 10: Safety Prerequisites Enforcement
*For any* advanced experiment requiring safety training, attempting to start the experiment without the required SafetyCertification should be blocked.

**Validates: Requirements 3.5**

### Property 11: Safety Violation Response
*For any* action that violates safety rules during an experiment, the system should pause the experiment and provide corrective Guidance.

**Validates: Requirements 3.7**

### Property 12: Asset Compression
*For any* image or media asset served by the system, the file size should be optimized to minimize bandwidth usage while maintaining acceptable quality.

**Validates: Requirements 4.2**

### Property 13: API Response Size Optimization
*For any* API response from the Backend, the payload size should be minimized through compression and efficient data structures.

**Validates: Requirements 4.5**

### Property 14: Offline State Preservation
*For any* experiment in progress, losing internet connectivity should preserve the current ExperimentState and allow continued interaction.

**Validates: Requirements 4.6, 10.1**

### Property 15: Equipment Tooltip Presence
*For any* piece of lab equipment in the Virtual_Lab, hovering over it should display a tooltip containing the equipment name and usage instructions.

**Validates: Requirements 5.2**

### Property 16: Invalid Action Feedback
*For any* invalid action attempted by a student, the system should provide immediate feedback explaining why the action is not allowed.

**Validates: Requirements 5.4**

### Property 17: Undo Functionality
*For any* experiment state after performing an action, invoking undo should revert to the previous state without requiring a full experiment restart.

**Validates: Requirements 5.7**

### Property 18: AI Tutor Context Access
*For any* student question asked during an experiment, the AI_Tutor should have access to the current ExperimentState for context-aware responses.

**Validates: Requirements 6.1**

### Property 19: Progress Record Completeness
*For any* completed experiment, the system should create a UserProgress record containing the experiment_id, completion_date, and performance score.

**Validates: Requirements 7.1, 7.2**

### Property 20: Progress Report Content
*For any* student's progress report, it should include lists of completed experiments, earned safety certifications, and skill development metrics.

**Validates: Requirements 7.3**

### Property 21: Experiment Categorization
*For any* experiment in the system, it should have assigned values for subject, grade_level, and curriculum_topic for proper organization.

**Validates: Requirements 8.1**

### Property 22: Experiment Card Information
*For any* experiment displayed in the library, the experiment card should show title, description, difficulty level, and estimated duration.

**Validates: Requirements 8.2**

### Property 23: Search Functionality
*For any* keyword search query, the system should return all experiments whose title, description, or topics contain the search term.

**Validates: Requirements 8.3**

### Property 24: Experiment Detail Display
*For any* selected experiment, the detail view should display learning objectives, required prior knowledge, and safety considerations.

**Validates: Requirements 8.4**

### Property 25: Completion Status Marking
*For any* experiment that a student has completed, the experiment should be marked as completed in the library view.

**Validates: Requirements 8.6**

### Property 26: Voice Mode Conversion
*For any* AI_Tutor response when voice mode is enabled, the text should be converted to speech using the Voice_Synthesizer in the selected language.

**Validates: Requirements 9.1**

### Property 27: Voice Output Language Consistency
*For any* text synthesized to speech, the Voice_Synthesizer should use a voice appropriate for the selected Language_Context.

**Validates: Requirements 9.2**

### Property 28: Audio Option Availability
*For any* experiment instruction displayed, an option to hear the instruction read aloud should be available.

**Validates: Requirements 9.4**

### Property 29: Local State Storage
*For any* ExperimentState when the system is offline, the state should be stored in browser local storage.

**Validates: Requirements 10.2**

### Property 30: Online Synchronization
*For any* locally stored data when connectivity is restored, the system should synchronize the data with the Backend without data loss.

**Validates: Requirements 10.3, 10.6**

### Property 31: Keyboard Navigation Support
*For any* interactive element in the Frontend, it should be accessible via keyboard navigation.

**Validates: Requirements 11.1**

### Property 32: Accessibility Attributes
*For any* interactive element or visual content, appropriate ARIA labels, alt text, or semantic HTML should be present for screen reader compatibility.

**Validates: Requirements 11.3, 11.5**

### Property 33: API Authentication
*For any* request received by the Backend, authentication and authorization should occur before processing the request.

**Validates: Requirements 12.2**

### Property 34: Secure Data Storage
*For any* user data, progress, or experiment results stored by the Backend, the data should be encrypted at rest and in transit.

**Validates: Requirements 12.5**

### Property 35: Error Response Format
*For any* API error condition, the Backend should return an appropriate HTTP status code and a structured error message.

**Validates: Requirements 12.6**

### Property 36: Rate Limiting
*For any* user making API requests, the system should enforce rate limits to prevent abuse.

**Validates: Requirements 12.7**

### Property 37: Request Logging
*For any* API request or error, the Backend should create a log entry for monitoring and debugging.

**Validates: Requirements 12.8**

### Property 38: Physics Formula Compliance
*For any* physics simulation, the calculated results should match the expected results from established scientific formulas within acceptable error margins.

**Validates: Requirements 13.1**

### Property 39: Stoichiometry Preservation
*For any* chemical reaction simulation, the stoichiometric ratios of reactants and products should be preserved according to the balanced equation.

**Validates: Requirements 13.2**

### Property 40: Measurement Uncertainty
*For any* measurement in an experiment, the system should include realistic measurement uncertainty and experimental error.

**Validates: Requirements 13.3**

### Property 41: Result Variation
*For any* experiment performed multiple times with the same parameters, the results should show natural variation within expected ranges.

**Validates: Requirements 13.4**

### Property 42: Input Validation
*For any* student input to the system, validation should occur to ensure the input is within realistic ranges and constraints.

**Validates: Requirements 13.6**

### Property 43: Time Acceleration Accuracy
*For any* time-dependent experiment with time acceleration enabled, the final results should match the results without acceleration within acceptable error margins.

**Validates: Requirements 13.7**

### Property 44: Experiment Definition Validation
*For any* new experiment added to the system, the experiment definition should be validated for completeness and correctness before being made available.

**Validates: Requirements 14.2**

### Property 45: Backward Compatibility
*For any* experiment that students have in progress, updating the experiment definition should not break the in-progress sessions.

**Validates: Requirements 14.6**

## Error Handling

### Error Categories

1. **Network Errors**
   - Connection timeout
   - Connection lost during operation
   - API endpoint unavailable
   - Rate limit exceeded

2. **Validation Errors**
   - Invalid user input
   - Malformed API request
   - Missing required parameters
   - Out-of-range values

3. **Simulation Errors**
   - Invalid action for current state
   - Physical constraint violation
   - Undefined behavior in simulation

4. **Authentication/Authorization Errors**
   - Invalid credentials
   - Expired session
   - Insufficient permissions
   - Missing safety prerequisites

5. **Data Errors**
   - Experiment definition not found
   - Corrupted state data
   - Failed to load assets
   - Database operation failure

### Error Handling Strategies

**Frontend Error Handling:**

```python
class ErrorHandler:
    """Centralized error handling for frontend"""
    
    def handle_error(self, error: Exception, context: dict) -> None:
        """
        Handle errors with appropriate user feedback
        
        Strategy:
        1. Log error details for debugging
        2. Determine error category
        3. Show user-friendly message in selected language
        4. Provide recovery options where possible
        5. Preserve user data/state
        """
        pass
    
    def handle_network_error(self, error: NetworkError) -> None:
        """
        Handle network-related errors
        
        Actions:
        - Switch to offline mode if possible
        - Queue operations for later sync
        - Show connectivity status
        - Suggest retry or continue offline
        """
        pass
    
    def handle_validation_error(self, error: ValidationError) -> None:
        """
        Handle input validation errors
        
        Actions:
        - Highlight invalid input
        - Show specific error message
        - Suggest valid input range
        - Preserve other valid inputs
        """
        pass
```

**Backend Error Handling:**

```python
class APIErrorHandler:
    """Centralized error handling for Lambda functions"""
    
    def handle_exception(self, exception: Exception, 
                        request_context: dict) -> dict:
        """
        Convert exceptions to API responses
        
        Returns:
        {
            "statusCode": int,
            "body": {
                "error": str,
                "message": str,
                "request_id": str
            }
        }
        """
        pass
    
    def log_error(self, error: Exception, context: dict) -> None:
        """Log error to CloudWatch with context"""
        pass
```

### Error Response Format

All API errors follow a consistent format:

```python
{
    "error": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
        "field": "specific_field_with_error",
        "reason": "detailed_reason"
    },
    "request_id": "unique_request_identifier",
    "timestamp": "ISO8601_timestamp"
}
```

### Retry Logic

```python
class RetryHandler:
    """Implements exponential backoff for retries"""
    
    def retry_with_backoff(self, operation: Callable, 
                          max_retries: int = 3,
                          base_delay: float = 1.0) -> Any:
        """
        Retry operation with exponential backoff
        
        Retry conditions:
        - Network timeout
        - 5xx server errors
        - Rate limit (with longer delay)
        
        No retry conditions:
        - 4xx client errors (except 429)
        - Authentication failures
        - Validation errors
        """
        pass
```

## Testing Strategy

### Dual Testing Approach

The system requires both unit testing and property-based testing for comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs

Both approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing

**Framework**: Use `hypothesis` library for Python property-based testing

**Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: ai-lab-simulator, Property {number}: {property_text}`

**Example Property Test:**

```python
from hypothesis import given, strategies as st
import pytest

# Feature: ai-lab-simulator, Property 3: Experiment Initialization Completeness
@given(experiment_def=st.builds(ExperimentDefinition))
def test_experiment_initialization_completeness(experiment_def):
    """
    For any experiment definition, starting the experiment should create
    an ExperimentState containing all equipment and materials specified.
    """
    lab = VirtualLab(experiment_def.experiment_id)
    state = lab.start_experiment()
    
    # Verify all equipment is initialized
    for equipment in experiment_def.equipment:
        assert equipment.id in state.equipment
        assert state.equipment[equipment.id].type == equipment.type
    
    # Verify all materials are initialized
    for material in experiment_def.materials:
        assert material.id in state.materials
        assert state.materials[material.id].quantity == material.quantity
```

### Unit Testing

**Framework**: Use `pytest` for Python unit testing

**Coverage Areas**:
- Specific experiment scenarios
- Edge cases (empty inputs, boundary values)
- Error conditions and exception handling
- Integration between components
- API endpoint behavior

**Example Unit Test:**

```python
def test_invalid_action_provides_feedback():
    """Test that invalid actions receive appropriate feedback"""
    lab = VirtualLab("circuit-basics")
    state = lab.start_experiment()
    
    # Try to connect incompatible components
    action = Action(
        action_type="connect",
        target="battery",
        parameters={"to": "thermometer"}  # Invalid connection
    )
    
    result = lab.perform_action(action)
    
    assert result.success == False
    assert result.feedback is not None
    assert "cannot connect" in result.feedback.lower()
    assert state == lab.state  # State unchanged
```

### Integration Testing

Test interactions between components:

```python
def test_ai_tutor_experiment_context_integration():
    """Test AI tutor can access experiment context"""
    lab = VirtualLab("acid-base-titration")
    state = lab.start_experiment()
    
    # Perform some actions
    lab.perform_action(Action("add", "acid", {"volume": 10}))
    
    # Ask AI tutor for help
    tutor = AITutor(language="english")
    response = tutor.ask_question(
        "What should I do next?",
        experiment_context=state.to_dict()
    )
    
    # Verify tutor has context
    assert "titration" in response.lower()
    assert "acid" in response.lower()
```

### Test Data Generation

Use `hypothesis` strategies for generating test data:

```python
from hypothesis import strategies as st

# Strategy for generating valid experiments
experiment_strategy = st.builds(
    Experiment,
    experiment_id=st.text(min_size=1, max_size=50),
    subject=st.sampled_from(['physics', 'chemistry', 'biology']),
    grade_level=st.integers(min_value=6, max_value=12),
    difficulty=st.sampled_from(['beginner', 'intermediate', 'advanced'])
)

# Strategy for generating valid actions
action_strategy = st.builds(
    Action,
    action_type=st.sampled_from(['move', 'mix', 'heat', 'measure', 'connect']),
    target=st.text(min_size=1),
    parameters=st.dictionaries(st.text(), st.text())
)

# Strategy for generating measurements
measurement_strategy = st.builds(
    Measurement,
    tool=st.sampled_from(['thermometer', 'ruler', 'ph_meter', 'multimeter']),
    value=st.floats(min_value=0, max_value=1000),
    unit=st.text(min_size=1),
    uncertainty=st.floats(min_value=0, max_value=10)
)
```

### Performance Testing

While not part of unit/property tests, performance should be validated:

- Load testing with locust or similar tools
- API response time monitoring
- Frontend rendering performance
- Database query optimization
- Lambda cold start optimization

### Accessibility Testing

- Automated accessibility testing with `axe-core`
- Manual testing with screen readers
- Keyboard navigation testing
- Color contrast validation
- WCAG 2.1 AA compliance verification

### Test Organization

```
tests/
├── unit/
│   ├── test_ai_tutor.py
│   ├── test_virtual_lab.py
│   ├── test_safety_simulator.py
│   ├── test_voice_synthesizer.py
│   └── test_offline_manager.py
├── property/
│   ├── test_language_properties.py
│   ├── test_experiment_properties.py
│   ├── test_safety_properties.py
│   ├── test_data_properties.py
│   └── test_simulation_properties.py
├── integration/
│   ├── test_ai_tutor_integration.py
│   ├── test_lab_workflow.py
│   └── test_offline_sync.py
├── e2e/
│   ├── test_complete_experiment.py
│   └── test_safety_certification.py
└── conftest.py  # Shared fixtures and configuration
```

### Continuous Integration

- Run all tests on every commit
- Property tests run with 100 iterations in CI
- Integration tests run against test AWS environment
- Code coverage target: 80% minimum
- All tests must pass before merge

## Implementation Notes

### Streamlit-Specific Considerations

1. **Session State Management**: Use `st.session_state` for maintaining state across reruns
2. **Caching**: Use `@st.cache_data` and `@st.cache_resource` for expensive operations
3. **Real-time Updates**: Use `st.rerun()` for dynamic updates
4. **Custom Components**: May need custom Streamlit components for complex visualizations

### AWS Lambda Best Practices

1. **Cold Start Optimization**: Keep dependencies minimal, use Lambda layers
2. **Connection Reuse**: Initialize AWS clients outside handler function
3. **Timeout Configuration**: Set appropriate timeouts (AI calls may need 30s+)
4. **Memory Allocation**: Tune memory based on function requirements
5. **Environment Variables**: Use for configuration (API keys, endpoints)

### Multilingual Implementation

1. **Translation Files**: Store translations in JSON files organized by language
2. **Fallback Language**: Default to English if translation missing
3. **RTL Support**: Consider right-to-left languages for future expansion
4. **Cultural Adaptation**: Use culturally appropriate examples and analogies

### Security Considerations

1. **API Authentication**: Use AWS Cognito JWT tokens
2. **Data Encryption**: Encrypt sensitive data at rest and in transit
3. **Input Sanitization**: Validate and sanitize all user inputs
4. **Rate Limiting**: Implement per-user rate limits
5. **CORS Configuration**: Restrict API access to known origins
6. **Secrets Management**: Use AWS Secrets Manager for API keys

### Cost Optimization

1. **Lambda Optimization**: Right-size memory and timeout
2. **DynamoDB**: Use on-demand pricing for variable load
3. **S3**: Use lifecycle policies for old data
4. **Bedrock**: Cache common AI responses
5. **Polly**: Cache frequently used audio
6. **CloudFront**: CDN for static assets reduces bandwidth costs

### Monitoring and Observability

1. **CloudWatch Logs**: Centralized logging for all Lambda functions
2. **CloudWatch Metrics**: Track API latency, error rates, usage
3. **X-Ray**: Distributed tracing for debugging
4. **Alarms**: Set up alarms for error rates, latency spikes
5. **Dashboards**: Create dashboards for key metrics

This design provides a comprehensive, production-ready architecture for Rupant AI that leverages Python throughout the stack, AWS serverless services, and follows best practices for scalability, accessibility, and educational effectiveness.
