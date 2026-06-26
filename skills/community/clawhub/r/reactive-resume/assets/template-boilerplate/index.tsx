// Reactive Resume 模板脚手架
// 复制此文件到 public/templates/[your-template]/index.tsx

import type { TemplateProps } from '@/types/template';

/**
 * 模板主组件
 * 
 * @param resume - 简历数据对象
 * @param theme - 主题配置
 * @returns React 组件
 */
export function BoilerplateTemplate({ resume, theme }: TemplateProps) {
  return (
    <div 
      className="template boilerplate"
      style={{ 
        fontFamily: theme.font,
        color: theme.text,
        backgroundColor: theme.background,
      }}
    >
      {/* 头部区域 */}
      <header className="template-header">
        <div className="header-content">
          <h1 className="name">{resume.basics?.name}</h1>
          <p className="headline">{resume.basics?.headline}</p>
          
          {/* 联系信息 */}
          <div className="contact-info">
            {resume.basics?.email && (
              <span className="email">{resume.basics.email}</span>
            )}
            {resume.basics?.phone && (
              <span className="phone">{resume.basics.phone}</span>
            )}
            {resume.basics?.location && (
              <span className="location">{resume.basics.location}</span>
            )}
          </div>
        </div>
      </header>

      {/* 主要内容区域 */}
      <main className="template-main">
        {/* 个人总结 */}
        {resume.basics?.summary && (
          <section className="section summary">
            <h2 className="section-title">Summary</h2>
            <p className="section-content">{resume.basics.summary}</p>
          </section>
        )}

        {/* 工作经历 */}
        {resume.work && resume.work.length > 0 && (
          <section className="section work">
            <h2 className="section-title">Work Experience</h2>
            <div className="work-list">
              {resume.work.map((work) => (
                <div key={work.id} className="work-item">
                  <div className="work-header">
                    <h3 className="position">{work.position}</h3>
                    <span className="company">{work.company}</span>
                  </div>
                  <div className="work-meta">
                    <span className="date">
                      {work.startDate} - {work.endDate || 'Present'}
                    </span>
                    {work.location && (
                      <span className="location">{work.location}</span>
                    )}
                  </div>
                  {work.summary && (
                    <p className="work-summary">{work.summary}</p>
                  )}
                  {work.highlights && work.highlights.length > 0 && (
                    <ul className="work-highlights">
                      {work.highlights.map((highlight, index) => (
                        <li key={index}>{highlight}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 项目经历 */}
        {resume.projects && resume.projects.length > 0 && (
          <section className="section projects">
            <h2 className="section-title">Projects</h2>
            <div className="projects-list">
              {resume.projects.map((project) => (
                <div key={project.id} className="project-item">
                  <div className="project-header">
                    <h3 className="name">{project.name}</h3>
                    {project.link && (
                      <a href={project.link} className="link">
                        {project.link}
                      </a>
                    )}
                  </div>
                  {project.description && (
                    <p className="description">{project.description}</p>
                  )}
                  {project.highlights && project.highlights.length > 0 && (
                    <ul className="highlights">
                      {project.highlights.map((highlight, index) => (
                        <li key={index}>{highlight}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 教育背景 */}
        {resume.education && resume.education.length > 0 && (
          <section className="section education">
            <h2 className="section-title">Education</h2>
            <div className="education-list">
              {resume.education.map((edu) => (
                <div key={edu.id} className="education-item">
                  <h3 className="institution">{edu.institution}</h3>
                  <div className="education-meta">
                    <span className="degree">{edu.area}</span>
                    <span className="study-type">{edu.studyType}</span>
                    <span className="date">
                      {edu.startDate} - {edu.endDate || 'Present'}
                    </span>
                  </div>
                  {edu.score && (
                    <span className="score">GPA: {edu.score}</span>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 技能 */}
        {resume.skills && resume.skills.length > 0 && (
          <section className="section skills">
            <h2 className="section-title">Skills</h2>
            <div className="skills-list">
              {resume.skills.map((skill) => (
                <div key={skill.id} className="skill-item">
                  <span className="skill-name">{skill.name}</span>
                  {skill.keywords && skill.keywords.length > 0 && (
                    <div className="skill-keywords">
                      {skill.keywords.map((keyword, index) => (
                        <span key={index} className="keyword">{keyword}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

/**
 * 模板配置
 */
export const templateConfig = {
  id: 'boilerplate',
  name: 'Boilerplate',
  description: 'A clean boilerplate template for customization',
  sizes: ['A4', 'Letter'] as const,
  theme: {
    primary: '#2563eb',
    secondary: '#64748b',
    text: '#1e293b',
    background: '#ffffff',
  },
  options: {
    showPhoto: true,
    showSummary: true,
    layout: 'single-column',
  },
};
