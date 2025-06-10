interface ScoreDisplayProps {
  score: number;
  suggestions: string[];
  sectionFeedback: {
    summary: string;
    skills: string;
    education: string;
    experience: string;
    grammar: string;
  };
}

export default function ScoreDisplay({ score, suggestions, sectionFeedback }: ScoreDisplayProps) {
  const getFeedbackColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'good':
        return 'bg-green-100 text-green-800';
      case 'okay':
        return 'bg-yellow-100 text-yellow-800';
      case 'missing':
      case 'poor':
      case 'needs improvement':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Score Circle */}
      <div className="flex justify-center">
        <div className="relative inline-flex">
          <div className="w-32 h-32 rounded-full bg-gray-100 flex items-center justify-center">
            <div className="text-4xl font-bold">{score}</div>
          </div>
          <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
            Score
          </div>
        </div>
      </div>

      {/* Section Feedback */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Section Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(sectionFeedback).map(([section, status]) => (
            <div key={section} className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="capitalize">{section}</span>
              <span className={`px-2 py-1 rounded-full text-sm ${getFeedbackColor(status)}`}>
                {status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Suggestions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Suggestions for Improvement</h3>
        <ul className="space-y-2">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="flex items-start">
              <svg
                className="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>{suggestion}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
} 