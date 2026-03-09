# 🧪 Rupant AI - AI-Powered Lab Simulator

> Democratizing science education for rural Indian schools through AI-powered virtual laboratories

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20Bedrock%20%7C%20Polly-orange.svg)](https://aws.amazon.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Overview

**Rupant AI** is a comprehensive virtual laboratory platform designed specifically for rural Indian schools with limited access to physical lab equipment and resources. The system combines multilingual AI tutoring, realistic experiment simulations, and comprehensive safety education to provide world-class science education to students in resource-constrained environments.

### 🎯 Key Features

- **🗣️ Multilingual AI Tutor**: Conversational AI support in Hindi, Tamil, Telugu, Bengali, Marathi, and English powered by Amazon Bedrock
- **🔬 Virtual Lab Experiments**: 20+ realistic experiments across Physics, Chemistry, and Biology aligned with CBSE curriculum
- **⚠️ Safety Simulator**: Interactive safety training scenarios covering chemical, electrical, fire, and biological hazards
- **🌐 Offline Capability**: Works with intermittent connectivity - experiments cached locally for uninterrupted learning
- **📊 Progress Tracking**: Comprehensive analytics and personalized learning recommendations
- **🔊 Voice Synthesis**: Text-to-speech in multiple Indian languages using Amazon Polly
- **📱 Low-Bandwidth Optimized**: Designed to work on 2G connections with minimal data usage

## 🚀 Why Rupant AI?

### The Problem
Rural Indian schools face significant challenges in science education:
- Limited or no access to physical laboratory equipment
- Lack of trained lab instructors
- Safety concerns with hazardous materials
- Language barriers in English-only educational content
- Poor internet connectivity

### Our Solution
Rupant AI addresses these challenges by providing:
- **Safe Learning Environment**: Students can experiment without physical risks
- **Accessible Education**: Works on basic hardware and slow internet connections
- **Culturally Relevant**: AI tutor explains concepts using local context and examples
- **Cost-Effective**: Serverless architecture scales efficiently without infrastructure costs
- **Inclusive Design**: Supports multiple Indian languages and accessibility features

## 🏗️ Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Student Browser                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Streamlit Frontend (Python)                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │ │
│  │  │ AI Tutor │  │ Virtual  │  │  Safety Simulator    │ │ │
│  │  │   UI     │  │  Lab UI  │  │       UI             │ │ │
│  │  └──────────┘  └──────────┘  └──────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS / REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS API Gateway                           │
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

### Technology Stack

**Frontend**
- Python 3.9+
- Streamlit for rapid web UI development
- Local storage for offline capability

**Backend**
- AWS Lambda (Python runtime) for serverless compute
- AWS API Gateway for RESTful endpoints
- Amazon DynamoDB for data persistence
- Amazon S3 for asset storage

**AI/ML Services**
- Amazon Bedrock (Claude model) for conversational AI
- Amazon Polly for text-to-speech synthesis

**Authentication & Security**
- AWS Cognito for user management
- IAM roles for secure service access

## 📚 Core Components

### 1. AI Tutor
- Context-aware assistance during experiments
- Multilingual support with language switching
- Culturally relevant explanations and examples
- Proactive hints when students are stuck
- Response time < 3 seconds

### 2. Virtual Lab
- **Physics**: Circuits, mechanics, optics experiments
- **Chemistry**: Reactions, titrations, pH measurements
- **Biology**: Microscopy, cell observation, dissection
- Realistic simulation based on scientific principles
- Measurement tools with appropriate precision
- Undo functionality for safe exploration

### 3. Safety Simulator
- Interactive scenarios for hazard training
- Chemical, electrical, fire, and biological safety
- Certification system for advanced experiments
- Real-time safety monitoring during experiments
- Corrective guidance for violations

### 4. Progress Tracking
- Experiment completion tracking
- Performance scoring and analytics
- Safety compliance monitoring
- Personalized learning recommendations
- Downloadable lab reports and certificates

## 🎓 Experiment Library

### Physics (10+ Experiments)
- Ohm's Law and Circuit Analysis
- Projectile Motion
- Reflection and Refraction
- Simple Pendulum
- And more...

### Chemistry (10+ Experiments)
- Acid-Base Titration
- Chemical Reactions
- pH Measurement
- Stoichiometry
- And more...

### Biology (10+ Experiments)
- Cell Observation under Microscope
- Plant Anatomy
- Dissection Simulations
- Enzyme Activity
- And more...

All experiments are:
- ✅ Aligned with CBSE curriculum (Grades 6-12)
- ✅ Available in 6 Indian languages + English
- ✅ Include safety protocols and learning objectives
- ✅ Generate comprehensive lab reports

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.9 or higher
python --version

# AWS CLI configured with credentials
aws --version

# pip for package management
pip --version
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rupant-ai.git
cd rupant-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure AWS credentials**
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Deployment

Deploy to AWS using the provided deployment scripts:

```bash
# Deploy backend Lambda functions
cd backend
python deploy.py

# Deploy frontend to AWS
cd ../frontend
streamlit deploy
```

## 📖 Usage

### For Students

1. **Select Language**: Choose your preferred language from the dropdown
2. **Browse Experiments**: Explore the experiment library by subject or grade level
3. **Complete Safety Training**: Earn certifications before advanced experiments
4. **Perform Experiments**: Follow step-by-step instructions with AI tutor assistance
5. **Track Progress**: View your completed experiments and performance metrics

### For Teachers

1. **Monitor Progress**: Access class-wide analytics and individual student reports
2. **Customize Content**: Adjust experiment parameters (admin access required)
3. **Review Safety Compliance**: Track student safety scores and violations
4. **Generate Reports**: Export progress reports and certificates

## 🌐 Multilingual Support

Rupant AI supports the following languages:

| Language | Code | Voice Support |
|----------|------|---------------|
| English | en | ✅ |
| Hindi | hi | ✅ |
| Tamil | ta | ✅ |
| Telugu | te | ✅ |
| Bengali | bn | ✅ |
| Marathi | mr | ✅ |

## 🔒 Security & Privacy

- **Data Encryption**: All data encrypted in transit (HTTPS) and at rest
- **Role-Based Access**: Student, teacher, and admin roles with appropriate permissions
- **Audit Logging**: All data access logged for security monitoring
- **Privacy Compliance**: Minimal PII collection, account deletion support
- **Rate Limiting**: API protection against abuse

## 📊 Performance

- **Response Time**: < 2 seconds for API requests
- **Concurrent Users**: Supports 1000+ simultaneous users
- **Offline Mode**: Full experiment functionality without internet
- **Low Bandwidth**: Works on 2G connections (< 5 seconds initial load)
- **Scalability**: Auto-scaling serverless architecture

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
black .

# Run type checking
mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Amazon Web Services** for cloud infrastructure and AI services
- **CBSE** for curriculum alignment guidelines
- **Rural schools** who provided feedback and testing
- **Open source community** for tools and libraries


## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core virtual lab functionality
- ✅ Multilingual AI tutor
- ✅ Safety simulator
- ✅ 20+ experiments

### Phase 2 (Planned)
- 🔄 Mobile app (iOS/Android)
- 🔄 Collaborative experiments (multi-student)
- 🔄 Teacher dashboard enhancements
- 🔄 Additional languages (Gujarati, Kannada, Malayalam)

### Phase 3 (Future)
- 📋 VR/AR experiment support
- 📋 Integration with Learning Management Systems
- 📋 Advanced analytics with ML insights
- 📋 Gamification and achievements

## 📈 Impact

Rupant AI aims to reach:
- **1 million+ students** in rural Indian schools
- **10,000+ schools** across India
- **50+ experiments** covering complete CBSE curriculum
- **10+ languages** for pan-India accessibility

---

<p align="center">
  <strong>Built with ❤️ for rural Indian students</strong>
  <br>
  <em>Empowering the next generation of scientists</em>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

"For detailed technical setup and AWS architecture, please see the Infrastructure Documentation."

"To run this project, ensure you have your AWS credentials configured locally using aws configure."

